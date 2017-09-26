# coding:utf-8
'''
    作者：SFLYQ
    功能：
        根据保险岛问问文章ID，批量爬取留言的代理人信息
    使用python模块:
        urllib2 发起请求，获取HTML
        PyQuery HTML解析
        threading 启动多线程
    申明：
        我分享的爬虫功能仅供学习参考，如果拿去私用所有产生的后果由使用者自己承担
'''

import os
import sys
import re
import threading
from pyquery import PyQuery as jquery
dir_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(dir_path + "/..")
import common.request as rq

proxyDatas = []


def getComment(questionNum):
    url = u'http://www.bxd365.com/qa/%s.html' % questionNum
    print u"开始解析:%s" % url
    try:
        html = rq.get(url)
    except Exception, e:
        print e
        return
    doc = jquery(html)
    replys = doc.find(".reply li")
    if replys is None:
        print u'无评论数据'
        return
    if len(replys) <= 0:
        print u'评论数量为0'
        return
    for item in replys:
        parseComment(questionNum, item)


def parseComment(questionNum, commentItem):
    if commentItem is None:
        print u'评论标签不存在'
        return
    commentJq = jquery(commentItem)
    # 机构
    organization = commentJq.find(".div1 .p1 span a").html()
    # 代理人
    proxy = commentJq.find(".div1 .p1 a span").html()
    # 回复内容
    replys = commentJq.find(".div2 p")
    if replys is None:
        print u'评论回复为空'
        return
    # 解析回复内容
    proxyReply = replys[0]
    if proxyReply is None:
        print u'无代理人回复'
        return
    proxyReplyJq = jquery(proxyReply)
    proxyReplyComment = proxyReplyJq.html()
    # 解析手机号
    proxyReplyComment = cnToNum(proxyReplyComment)
    proxyReplyComment = proxyReplyComment.replace(u"-", "")
    proxyReplyComment = proxyReplyComment.replace(u"_", "")
    proxyReplyComment = proxyReplyComment.replace(u"—", "")
    phone = parsePhone(proxyReplyComment)
    saveHandle(questionNum,
               {"proxy": proxy,
                "organization": organization,
                "phone": phone})
    return


def parsePhone(content):
    '''
        解析手机号
    '''
    if content is None:
        return None
    re_phone = re.search(r'[1][3,4,5,7,8][0-9]{9}', content, re.S)
    phoneNum = None
    if re_phone:
        phoneNum = re_phone.group()
    return phoneNum


def cnToNum(content):
    if content is None:
        return content
    content = content.replace(u"一", "1")
    content = content.replace(u"二", "2")
    content = content.replace(u"三", "3")
    content = content.replace(u"四", "4")
    content = content.replace(u"五", "5")
    content = content.replace(u"六", "6")
    content = content.replace(u"七", "7")
    content = content.replace(u"八", "8")
    content = content.replace(u"九", "9")
    content = content.replace(u"零", "0")
    return content


def saveHandle(questionNum, data):
    if data is None:
        print u'无法解析出代理人回复内容，跳过'
        return
    proxy = data['proxy']
    organization = data['organization']
    phone = data['phone']
    # 输出信息
    print organization, proxy, phone
    if phone is None:
        print u'无可用手机号'
        return
    # 校验是否存在
    if phone in proxyDatas:
        print u'手机号存在记录中'
        return
    # 写文件保存
    data_path = os.path.split(os.path.realpath(__file__))[0] + "\\datas\\"
    if not os.path.isdir(data_path):
        os.makedirs(data_path)
    f = open('%sdatas.txt' % (data_path), 'a')
    content = (u"问问ID：%s,机构：%s,代理人：%s,手机号：%s\n" % (questionNum, organization,
                                                   proxy, phone))
    f.write(content.encode("utf-8"))
    f.close()
    proxyDatas.append(phone)
    print u'保存代理人和手机号成功'


# 260000
def goHandle(snum, enum):
    if snum > enum:
        print 'sum不能大于enum'
        return

    for num in range(snum, enum):
        getComment(num)


def init(snum, enum, section):
    threads = []
    while snum < enum:
        end = snum + section
        if end > enum:
            end = enum
        t = threading.Thread(target=goHandle, args=(snum, end))
        print u'添加线程处理区间:%s-%s' % (snum, end)
        threads.append(t)
        snum = end
    print "go"
    for t in threads:
        t.setDaemon(True)
        t.start()
    # 等待所有线程完成
    for t in threads:
        t.join()
    print 'over'


init(200000, 260000, 2000)
# getComment(200012)