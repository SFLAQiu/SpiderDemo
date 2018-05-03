# coding:utf-8
'''
    作者：SFLYQ
    功能：
        生成短链地址，支持随机
    申明：
        我分享的爬虫功能仅供学习参考，如果拿去私用所有产生的后果由使用者自己承担
'''
import os
import sys
dir_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(dir_path + "/..")
import commons.request as rq
import json
import random


def suo(url):
    '''
        suo.im 短链
    '''
    url = 'http://suo.im/api.php?format=json&url={}'.format(
        url.encode('utf-8'))
    json_str = rq.get(url)
    if not json_str:
        return
    json_data = json.loads(json_str)
    return json_data['url']


def zhihu(url):
    '''
        知乎短链
    '''
    url = 'https://link.zhihu.com/?target={}'.format(url)
    return url


def ft12(url):
    '''
        ft12
    '''
    types = [1, 4, 5, 6, 7]
    count = len(types)
    sel_type = random.randint(0, count - 1)
    api_url = 'http://www.ft12.com/create.php?m=index&a=urlCreate'
    try:
        html = rq.post(api_url, {
            'url': url.encode('utf-8'),
            'type': types[sel_type]
        })
    except Exception as ex:
        print(ex)
        return
    json_data = json.loads(html)
    url = json_data['list']
    return url


def random_url(url):
    '''
        随机短链地址
    '''
    random_fn = [suo, zhihu, ft12]
    count = len(random_fn)
    index = random.randint(0, count - 1)
    fn = random_fn[index]
    url = fn(url)
    return url


print(random_url('http://www.baidu.com'))
print(ft12('http://www.baidu.com'))
print(suo('http://www.baidu.com'))