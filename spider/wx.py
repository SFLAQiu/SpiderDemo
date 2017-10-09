# coding:utf-8
'''
    作者：SFLYQ
    功能：
        爬取微信公众号所有文章留言板内容(代码有限制只获取2017的文章)
    申明：
        我分享的爬虫功能仅供学习参考，如果拿去私用所有产生的后果由使用者自己承担
'''

import os
import sys
import json
import urllib
import re
import time
dir_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(dir_path + "/..")
import common.request as rq
import common.helper as hp

articleDatas = []
proxyDatas = []
data_path = os.path.split(os.path.realpath(__file__))[0] + "\\datas\\"
wx_source = u'人民保险鼎'
biz = 'MzU0MjAxNTc4OQ%3D%3D'


def getArticle(offset):
    '''
        获取文章列表
    '''
    print u'页码：%s' % offset
    url = 'http://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=' + biz + '&f=json&offset=' + str(
        offset) + '&count=10&f=json'
    dataStr = rq.get_cookie(url, cookie_file_name="wx")
    # print dataStr
    dataJson = json.loads(dataStr)
    if dataJson["errmsg"] != 'ok':
        print u'获取数据返回:%s' % dataJson["errmsg"]
        return
    next_offset = dataJson["next_offset"]
    # 文章列表
    if offset == next_offset:
        print u'已经是没有翻页数据'
        return
    general_msg_list_str = dataJson["general_msg_list"]
    general_msg_list_json = json.loads(general_msg_list_str)
    article_list = general_msg_list_json["list"]
    # print article_list
    for item in article_list:
        # 获取文章发布时间
        publish_timestamp = item['comm_msg_info']['datetime']
        publish_time = time.localtime(publish_timestamp)
        # 校验文章发布时间
        if publish_time.tm_year < 2017:
            print u'超过限定日期，不继续捕获分页数据'
            return
        if not item.has_key('app_msg_ext_info'):
            continue
        # 文章标题
        item_title = item['app_msg_ext_info']['title']
        # 文章地址
        item_url = item['app_msg_ext_info']['content_url']
        # 获主文章
        articleDatas.append({
            'title': item_title,
            'url': item_url,
            'time': time.strftime("%Y-%m-%d", publish_time)
        })
        if item['app_msg_ext_info']['multi_app_msg_item_list'] is None:
            continue
        # 子文章
        for multi_item in item['app_msg_ext_info']['multi_app_msg_item_list']:
            item_title = multi_item['title']
            item_url = multi_item['content_url']
            articleDatas.append({
                'title': item_title,
                'url': item_url,
                'time': time.strftime("%Y-%m-%d", publish_time)
            })
    # 延迟
    hp.sleep(1, 3)
    getArticle(next_offset)


def getCommetDatas(url):
    '''
        获取评论JSON数据
        * 'url' 文章地址
    '''
    try:
        htmlStr = rq.get_cookie(url, cookie_file_name="wx")
        htmlStr = u'%s' % htmlStr
    except Exception, ex:
        print ex
        return
    # 解析获取请求留言接口需要的参数
    mid = re.search(r'mid=([\d]+)', url, re.S).groups()[0]
    biz = re.search(r'__biz=([^&]+)', url, re.S).groups()[0]
    re_comment_id = re.search(r'comment_id = "([\d]+)"', htmlStr, re.S)
    comment_id = None
    if re_comment_id:
        comment_id = re_comment_id.groups()[0]
    print u"文章ID=%s,biz=%s,留言板ID=%s" % (mid, biz, comment_id)
    if comment_id is None:
        print u'comment_id不存在'
        return
    # 请求留言接口
    api_url = 'http://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&__biz=%s&appmsgid=%s&idx=1&comment_id=%s&offset=0&limit=100' % (
        biz, mid, comment_id)
    commonDataStr = None
    try:
        commonDataStr = rq.get_cookie(
            api_url,
            cookie_file_name="wx",
            headers={
                "User-agent":
                "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"
            })
    except Exception, ex:
        print ex
        return
    # 解析留言数据为JSON格式

    if commonDataStr.find(u'请在微信客户端打开链接') > -1:
        print u'请在微信客户端打开链接'
        return
    commonDataJson = json.loads(commonDataStr)
    return commonDataJson


def analysisComment(article, comment):
    '''
        解析留言JSON数据，解析出手机号
        * 'article' 文章信息对象
        * 'comment' 留言json对象
    '''
    if comment is None:
        saveContent = u'标题：%s,地址：%s,无法抓取原因：无评论数据\n' % (article['title'],
                                                       article['url'])
        hp.write_to_file(data_path, 'err.txt', saveContent)
        print u"无评论数据"
        return
    print u''
    if not comment.has_key('elected_comment'):
        saveContent = u'标题：%s,地址：%s,无法抓取原因：评论无elected_comment数据\n' % (
            article['title'], article['url'])
        hp.write_to_file(data_path, 'err.txt', saveContent)
        print u"评论无elected_comment数据"
        return
    elected_comment = comment['elected_comment']
    print article['time'], article['title']
    for comment_item in elected_comment:
        try:
            print u''
            nick_name = comment_item['nick_name']
            content = comment_item['content']
            print u'微信名：%s,回复内容：%s' % (nick_name, content)
            phone = hp.parsePhone(nick_name)
            if phone is None:
                print u'无解析出手机号'
                continue
            print u'解析出手机号:%s' % phone
            # 校验是否存在
            if phone in proxyDatas:
                print u'手机号存在记录中'
                return
            # 写文件保存

            saveContent = u"来自文章(%s)：%s,微信昵称：%s,手机号：%s \n" % (article['time'],
                                                              article['title'],
                                                              nick_name, phone)
            hp.write_to_file(data_path, u'wx_datas_%s.txt' % wx_source,
                             saveContent)
            print u'保存手机号成功'
        except Exception, ex:
            print ex


def showArticle():
    '''
        遍历展示输出文章列表
    '''
    if articleDatas is None:
        return
    for item in articleDatas:
        print item['title'], urllib.unquote(item["url"]).replace("&amp;", "&")


def doCommentHandle():
    '''
        文章遍历解析留言板手机号数据
    '''
    article_count = len(articleDatas)
    if article_count <= 0:
        print u'无文章数据'
    print u"获取到文章总数:%s" % article_count
    # showArticle()
    # 遍历文章数据，进行留言数据的解析获取
    for index, item in enumerate(articleDatas):
        url = urllib.unquote(item["url"]).replace("&amp;", "&")
        print u"第(%s),开始解析文章地址：%s" % (index, url)
        # 获取留言的JSON数据
        commonDataJson = getCommetDatas(url)
        # 解析留言
        analysisComment(item, commonDataJson)
        # 延迟，感觉太快会被限制请求
        hp.sleep(1, 2.5)


def init():
    # 捕获文章信息
    getArticle(0)
    # 遍历文章,获取评论
    doCommentHandle()
    print u"完成所有解析~"


# getArticle(0)
# print len(articleDatas)
init()

# article_item_data = {
#     'title':
#     'test',
#     'url':
#     'http://mp.weixin.qq.com/s?__biz=MjM5NjY0MTIzMw==&mid=2649625702&idx=1&sn=db120c36d6e68515cb29037f92ea0b0f&chksm=befc94d8898b1dcebc35b44f7ab942b10e493857e3dcc425fc2d85a46ac3be47da07c694d948&scene=27#wechat_redirect'
# }
# data = getCommetDatas(article_item_data['url'])
# analysisComment(article_item_data, data)
