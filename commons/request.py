# coding:utf-8
import urllib
import os
import imghdr
import json
import http
from http import cookiejar
from enum import Enum
__cookie = None


class ECookieType(Enum):
    '''
        cookie模式
    '''

    MozillaCookieJar = 1
    "urllib MozillaCookieJar模式"
    CookieJar = 2
    "urllib CookieJar模式"


def get(url, headers={}, decode='utf-8', timeout=10):
    '''
        get请求   
        * 'url' 请求地址    
        * 'headers' 请求头字典    
        * 'timeout' 请求过期时间
    '''
    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request, timeout=timeout)
        response.encoding = 'utf-8'

        if decode is not None:
            return response.read().decode(decode)
        return response.read()
    except Exception as ex:
        print(u'请求接口', url, u'报错:', ex)
        return None


def post(url, data={}, headers={}, decode='utf-8'):
    '''
        post请求
        * 'url' 请求地址    
        * 'headers' 请求头字典    
        * 'data' post参数
    '''
    try:
        request = urllib.request.Request(url, headers=headers)
        data = urllib.parse.urlencode(data).encode(encoding='UTF8')
        response = urllib.request.urlopen(request, data=data)
        if decode is not None:
            return response.read().decode(decode)
        return response.read()
    except Exception as ex:
        print(u'request-post err:', ex)


def __create_init(cookie_file_name="default",
                  dir_path=None,
                  cookie_type=ECookieType.MozillaCookieJar,
                  init_cookies=None,
                  proxy=None):
    '''
        创建请求基础方法
    '''
    if cookie_type == ECookieType.MozillaCookieJar:
        cookie = __creacte_cookie_Mozilla(dir_path, cookie_file_name)
    if cookie_type == ECookieType.CookieJar:
        cookie = __creacte_cookie_jar(init_cookies)
    cookie_handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(cookie_handler)
    if proxy is not None:
        proxy_handler = urllib.request.ProxyHandler({
            'http':
            u'%s:%s' % (proxy['ip'], proxy['port'])
        })
        opener = urllib.request.build_opener(cookie_handler, proxy_handler)
    return opener, cookie


def __creacte_cookie_jar(init_cookies=None):
    '''
        创建CookieJar
        * 'init_cookies' 初始化cookie集合数据
    '''
    global __cookie
    if __cookie is None:
        __cookie = cookiejar.CookieJar()
    # 初始化cookie值
    if init_cookies is not None and len(init_cookies) > 0:
        for item in init_cookies:
            cookie_item = make_cookie(item['domain'], item['name'],
                                      item['value'])
            __cookie.set_cookie(cookie_item)
    return __cookie


def make_cookie(domain, name, value):
    '''
        创建cookie
        * 'domain' 域
        * 'name' cookie名
        * 'value' cookie值
    '''
    return cookiejar.Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain=domain,
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest=None)


def __creacte_cookie_Mozilla(dir_path, cookie_file_name):
    '''
        创建MozillaCookieJar
        * 'dir_path' 本地存储路径
        * 'cookie_file_name' 存储文件名
    '''
    if dir_path is None:
        dir_path = os.path.split(os.path.realpath(__file__))[0]
        dir_path = os.path.join(dir_path, 'cookie')
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    filename = os.path.join(dir_path, '%s.txt' % cookie_file_name)
    cookie = cookiejar.MozillaCookieJar(filename)
    if (os.path.exists(filename)):
        cookie.load(filename, ignore_discard=True, ignore_expires=True)
    return cookie


def post_cookie(url,
                data,
                dir_path=None,
                cookie_file_name="default",
                headers={
                    "User-agent":
                    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"
                },
                decode='utf-8',
                save_cookie=True,
                cookie_type=ECookieType.MozillaCookieJar,
                init_cookies=None,
                proxy=None,
                timeout=10):
    '''
        post请求，会自动带上cookie，如果有需要可以自己去初始化cookie文件里的cookie值
        * 'url' 请求的url地址
        * 'data' post参数
        * 'dir_path' cookie路径
        * 'cookie_file_name' cookie文件名，不需要包括文件拓展名
        * 'headers' 自定义请求头
        * 'decode' 字符串编码
        * 'save_cookie' 是否需要文件存储cookie, MozillaCookieJar 模式下支持
        * 'cookie_type' 使用cookie模式类型
        * 'init_cookies' 初始化cookie数据CookieJar模式下支持
        * 'proxy' 代理信息 dirct {ip,port,service}
        * 'timeout' 请求过期时间
    '''
    try:
        initObj = __create_init(
            cookie_file_name,
            dir_path=dir_path,
            cookie_type=cookie_type,
            init_cookies=init_cookies,
            proxy=proxy)
        opener = initObj[0]
        cookie = initObj[1]
        content_type = ''
        # 校验Content-Type 类型，构造对应的类型参数

        if 'Content-Type' in headers and headers['Content-Type'] is not None:
            content_type = str(headers['Content-Type'])
        if content_type.find('application/json') >= 0:
            params = json.dumps(data)
        else:
            params = urllib.parse.urlencode(data)
        params = params.encode(encoding='UTF8')
        req = urllib.request.Request(url, params, headers)
        response = opener.open(req, timeout=timeout)
        # MozillaCookieJar是否需要把cookie信息存文件中存储
        if save_cookie and cookie_type == ECookieType.MozillaCookieJar:
            cookie.save(ignore_discard=True, ignore_expires=True)
        if decode is not None:
            return response.read().decode(decode)
        return response.read()
    except Exception as ex:
        print(u'request-post-cookie err:', ex)


def get_cookie(url,
               dir_path=None,
               cookie_file_name="default",
               headers={
                   "User-agent":
                   "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"
               },
               decode='utf-8',
               save_cookie=True,
               cookie_type=ECookieType.MozillaCookieJar,
               init_cookies=None,
               proxy=None,
               timeout=10):
    '''
        get请求，会自动带上cookie，如果有需要可以自己去初始化cookie文件里的cookie值
        * 'url' 请求的url地址
        * 'dir_path' cookie路径
        * 'cookie_file_name' cookie文件名，不需要包括文件拓展名
        * 'headers' 自定义请求头
        * 'decode' 字符串编码
        * 'save_cookie' 是否需要文件存储cookie, MozillaCookieJar 模式下支持
        * 'cookie_type' 使用cookie模式类型
        * 'init_cookies' 初始化cookie数据CookieJar模式下支持
        * 'proxy' 代理信息 dirct {ip,port,service}
        * 'timeout' 请求过期时间
    '''
    initObj = __create_init(
        cookie_file_name,
        dir_path=dir_path,
        cookie_type=cookie_type,
        init_cookies=init_cookies,
        proxy=proxy)
    opener = initObj[0]
    cookie = initObj[1]
    req = urllib.request.Request(url, headers=headers)
    response = opener.open(req, timeout=timeout)
    # MozillaCookieJar是否需要把cookie信息存文件中存储
    if save_cookie and cookie_type == ECookieType.MozillaCookieJar:
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
        * 'decode' 字符串编码
        * 'cookie_file_name' cookie文件名
    '''
    content = get_cookie(
        url, headers=headers, cookie_file_name=cookie_file_name, decode=decode)
    imgtype = imghdr.what('', h=content)
    if not os.path.isdir(path):
        os.makedirs(path)
    if not imgtype:
        imgtype = extension
    file_path = u'%s/%s.%s' % (path, file_name, imgtype)
    with open(file_path, 'wb') as f:
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
    return urllib.parse.urlencode(data)


def url_quote(content):
    '''
        URL编码
    '''
    if not content:
        return
    content_quote = urllib.parse.quote(content)
    return content_quote