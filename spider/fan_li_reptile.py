# coding:utf-8
'''
    作者：SFLYQ
    功能：
        Demo1 抓取返利网品牌信息,简单入门Demo
    使用python模块:
        urllib2 发起请求，获取HTML
        PyQuery HTML解析
    申明：
        我分享的爬虫功能仅供学习参考，如果拿去私用所有产生的后果由使用者自己承担
'''

import urllib2
from pyquery import PyQuery as jquery


# 爬虫Demo1 爬虫返利网的品牌数据
class FanLiReptile:
    _url = 'http://www.fanli.com/'

    # 获取返利网品牌数据
    def GetBrandData(self):
        rs = urllib2.urlopen(self._url, timeout=10)
        html = rs.read().decode('utf-8')
        doc = jquery(html)
        brandJqs = doc.find('.super-mod')
        allNum = brandJqs.length  # 总数量
        print('解析出总的品牌数据量：%s' % allNum)
        scNum = 0  # 成功数据量
        for brandItem in brandJqs:
            brandJq = jquery(brandItem)
            if (len(brandJq.find('.mod-intro')) == 0):
                print('解析没有mod-intro标签')
                continue
            scNum += 1
            print brandJq.find('.mod-intro').html()
        print('成功获取的品牌数据数量：%s,解析失败数量:%s' % (scNum, allNum - scNum))


# Run爬虫
flr = FanLiReptile()
# 抓取返利品牌返
flr.GetBrandData()
