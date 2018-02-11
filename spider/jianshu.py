# coding:utf-8
'''
    作者：SFLYQ
    功能：
        简书专题文章内容爬虫
    说明：
        爬取简书【程序员】专题的文章列表，过滤出点击量，评论数量，收藏量高的文章
        爬取符合规则的文章内容，将文章内容html转Makedown编码，提交到redis队列
        （提交到redis后根据需求去使用，我这里是有程序对队列进行消耗，然后提交到自己bbs分享文章）
    申明：
        我分享的爬虫功能仅供学习参考，如果拿去私用所有产生的后果由使用者自己承担
'''
import os
import sys
# import threading
from pyquery import PyQuery as jquery
dir_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(dir_path + "/..")
import common.request as rq
import common.helper as hp
# import re
# import time
import html2text
import redis
import json
import datetime

# import common.dingding as ding
# 简述地址前缀
__jianshu_host = 'http://www.jianshu.com'
# 最新评论地址
__special_newlike_url = 'http://www.jianshu.com/c/{0}?order_by=commented_at&page=1'
# 专题标识
__specials = [{'title': u'程序员', 'key': 'NEt52a'}]
# 缓存记录
__cache_records_key = 'reptile:records'
# 缓存当前文章内容
__cache_current_key = 'reptile:current_contents'
# 我的redis本地服务器配置
__redis_config = {'host': '127.0.0.1', 'port': 6379, 'password': '123456'}
__r = redis.Redis(
    host=__redis_config['host'],
    port=__redis_config['port'],
    password=__redis_config['password'],
    db=0)


def specialArticles(key, source, page=1):
    '''
        获取主题中的文章信息列表
        * 'key' 主题Key
        * 'page' 文章页码
    '''
    url = __special_newlike_url.format(key)
    htmlStr = rq.get(url)
    if (not htmlStr):
        print u'获取html失败'
        return
    jq_dom = jquery(htmlStr)
    if (not jq_dom):
        print u'无法解析页面dom'
        return
    dom_contents = jq_dom.find('.content')
    if (not dom_contents):
        print u'无法解析文章内容'
        return
    articles = []
    for item in dom_contents:
        jq_content_item = jquery(item)
        dom_title = jq_content_item.find('.title')
        dom_time = jq_content_item.find('.time')
        dom_read = jq_content_item.find('.ic-list-read')
        dom_comments = jq_content_item.find('.ic-list-comments')
        dom_like = jq_content_item.find('.ic-list-like')
        if (not dom_title):
            print u'无法解析 title'
            continue
        if (not dom_time):
            print u'无法解析 time'
            continue
        # 解析文章信息
        article_read = int(dom_read.parent().text())
        article_comments = int(dom_comments.parent().text())
        article_like = int(dom_like.parent().text())
        article_title = dom_title.html()
        artitle_href = dom_title.attr('href')
        artitle_time = dom_time.attr('data-shared-at').replace(
            '-', ' ').replace('+08:00', '').replace('T', ' ')
        # artitle_time = time.strptime(artitle_time, '%Y %m %d %H:%M:%S')
        article_url = '{host}{href}'.format(
            host=__jianshu_host, href=artitle_href)
        print u'获得文章：', hp.remove_emoji(
            article_title), article_url, artitle_time
        if (article_read < 100):
            print u'文章阅读量<100，不爬取'
            continue
        if (article_like < 1):
            print u'文章收藏量<10，不爬取'
            continue
        if (article_comments < 1):
            print u'文章评论量<3，不爬取'
            continue
        # 获取文章内容
        content_html = getArticleContent(article_url)
        if (not content_html):
            print u'无法获取博文内容'
            continue
        # 文章内容字符串处理
        content_html = content_html.replace('data-original-', '')
        content_markdown = getCotentMarkDown(content_html)
        # markdown内容字符串处理
        #content_markdown = content_markdown.replace("|", "-")
        articles.append({
            'title': article_title,
            'url': article_url,
            'time': artitle_time,
            'source': source,
            'content': content_markdown
        })
    return articles


def getArticleContent(url):
    '''
        获取文章博文内容
    '''
    # show-content
    if (not url):
        print '非法地址'
        return
    htmlStr = rq.get(url)
    jq_dom = jquery(htmlStr)
    jq_content = jq_dom.find('.show-content')
    content_html = jq_content.html()
    # print content_html
    return content_html


def getCotentMarkDown(content):
    '''
        html转MarkDown
    '''
    if (not content):
        return content
    htmlStr = html2text.html2text(content)
    return htmlStr


def getAllSpecialArticles():
    '''
        获取所有主题文章列表
    '''
    allArticles = []
    for special in __specials:
        title = special['title']
        key = special['key']
        print u'开始爬:%s' % title
        articles = specialArticles(key, title)
        allArticles += articles
    return allArticles


def checkNeed():
    '''
        检验是否需要继续爬取
    '''
    current_len = __r.llen(__cache_current_key)
    if current_len and current_len > 10:
        return False
    return True


def pushArticle(articles):
    '''
        上报文章内容
    '''
    if not articles:
        print u'需要存储的articles为空'
        return
    for item in articles:
        jsonStr = json.dumps(item)
        rs = __r.hset(__cache_records_key, item['url'], 1)
        add_expire(__cache_records_key, 7)
        if (rs > 0):
            __r.lpush(__cache_current_key, jsonStr)
            add_expire(__cache_current_key, 0.5)
        rsStr = u'bingo' if (rs > 0L) else u'存在'
        print u'push文章', item['title'], rsStr


def add_expire(chache_name, expire_days):
    '''
        添加缓存过期时间
    '''
    ttl = __r.ttl(chache_name)
    if not ttl:
        __r.expire(chache_name, datetime.timedelta(days=expire_days))


def main():
    need = checkNeed()
    if need:
        try:
            articles = getAllSpecialArticles()
            print u'获取到文章总数:%s' % len(articles)
            pushArticle(articles)
        except Exception, ex:
            print u'err %s' % ex
    else:
        print u'文章还没有被消耗，我休息下爬'
    # 继续爬取文章
    hp.sleep_minute(60, u"文章爬取间隔")
    main()


main()

# content_html = getArticleContent('http://www.jianshu.com/p/594d1984fbd9')
# content_html = content_html.replace("-", "|")
# content_markdown = getCotentMarkDown(content_html)
# content_markdown = content_markdown.replace("_", "-")

# content_html = getArticleContent('http://www.jianshu.com/p/c0e5c13d5ecb')
# content_html = content_html.replace('data-original-', '')
# content_markdown = getCotentMarkDown(content_html)
# print content_markdown
# # markdown内容字符串处理
# content_markdown = content_markdown.replace("|", "-")
# print getCotentMarkDown(contentStr)
# pushArticle([{'title': 'aaa', 'url': 'vbvv'}])
