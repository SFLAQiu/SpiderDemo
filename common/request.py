# coding:utf-8

import urllib2
import urllib
import cookielib
import os
import imghdr


def get(url, headers={}, decode='utf-8'):
    '''
        get请求   
        * 'url' 请求地址    
        * 'headers' 请求头字典    
    '''
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    response.encoding = 'utf-8'

    if decode is not None:
        return response.read().decode(decode)
    return response.read()


def post(url, data={}, headers={}, decode='utf-8'):
    '''
        post请求
        * 'url' 请求地址    
        * 'headers' 请求头字典    
        * 'data' post参数
    '''
    request = urllib2.Request(url, headers=headers)
    data = urllib.urlencode(data)
    response = urllib2.urlopen(request, data=data)
    if decode is not None:
        return response.read().decode(decode)
    return response.read()


def __create_init(cookie_file_name="default", dir_path=None):
    '''
        创建请求基础方法
    '''
    if dir_path is None:
        dir_path = '%s\\cookie' % os.path.split(os.path.realpath(__file__))[0]
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    filename = '%s\\%s.txt' % (dir_path, cookie_file_name)
    cookie = cookielib.MozillaCookieJar(filename)
    if (os.path.exists(filename)):
        cookie.load(filename, ignore_discard=True, ignore_expires=True)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    return opener, cookie


def post_cookie(url,
                data,
                dir_path=None,
                cookie_file_name="default",
                headers={},
                decode='utf-8'):
    '''
        post请求，会自动带上cookie，如果有需要可以自己去初始化cookie文件里的cookie值
        * 'url' 请求的url地址
        * 'data' post参数
        * 'dir_path' cookie路径
        * 'cookie_file_name' cookie文件名，不需要包括文件拓展名
        * 'headers' 自定义请求头
    '''
    initObj = __create_init(cookie_file_name, dir_path=dir_path)
    opener = initObj[0]
    cookie = initObj[1]
    params = urllib.urlencode(data)
    req = urllib2.Request(url, params, headers)
    response = opener.open(req)
    cookie.save(ignore_discard=True, ignore_expires=True)
    if decode is not None:
        return response.read().decode(decode)
    return response.read().decode('utf-8')


def get_cookie(url,
               dir_path=None,
               cookie_file_name="default",
               headers={
                   "User-agent":
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"
               },
               decode='utf-8'):
    '''
        get请求，会自动带上cookie，如果有需要可以自己去初始化cookie文件里的cookie值
        * 'url' 请求的url地址
        * 'dir_path' cookie路径
        * 'cookie_file_name' cookie文件名，不需要包括文件拓展名
        * 'headers' 自定义请求头
    '''
    initObj = __create_init(cookie_file_name, dir_path=dir_path)
    opener = initObj[0]
    cookie = initObj[1]
    req = urllib2.Request(url, headers=headers)
    response = opener.open(req)
    cookie.save(ignore_discard=True, ignore_expires=True)
    if decode is not None:
        return response.read().decode(decode)
    return response.read()


def down_image(url,
               path,
               file_name,
               extension="jpg",
               headers={
                   "User-agent":
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"
               },
               decode='utf-8',
               cookie_file_name="default"):
    '''
        图片下载
        * 'url' 图片url地址
        * 'path' 图片存储路径
        * 'file_name' 图片存储文件名
        * 'extension' 图片存储拓展名
        * 'headers' 自定义请求头
    '''
    content = get_cookie(
        url, headers=headers, cookie_file_name=cookie_file_name, decode=decode)
    imgtype = imghdr.what('', h=content)
    if not os.path.isdir(path):
        os.makedirs(path)
    if not imgtype:
        imgtype = extension
    with open(u'{}\\{}.{}'.format(path, file_name, imgtype), 'wb') as f:
        f.write(content)


def get_query_parames(data):
    '''
        获取url参数
        * 'data' 数据字典
    '''
    if data is None:
        return None
    if not isinstance(data, dict):
        return None
    return urllib.urlencode(data)