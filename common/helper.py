# coding:utf-8
import os
import re
import random
import time
import hashlib
import functools
import zipfile
import datetime
import threading
import urllib
'''
    文件帮助
'''


def write_to_file(path, file_name, content, mode='a'):
    '''
        写内容到文件
        * 'path' 路径
        * 'file_name' 文件名，需要包括文件拓展名
        * 'content' 内容
        * 'mode' r=只读,w=只写,a=追加,r+,w+,a+
    '''
    if not os.path.isdir(path):
        os.makedirs(path)
    file_path = os.path.join(path, file_name)
    f = open(file_path, mode)
    f.write(content)
    f.close()


def read_from_file(path, file_name, mode='r'):
    '''
        读文件内容
        * 'path' 路径
        * 'file_name' 文件名，需要包括文件拓展名
        * 'mode' r=只读,w=只写,a=追加,r+,w+,a+
    '''
    if not os.path.isdir(path):
        os.makedirs(path)
    file_path = os.path.join(path, file_name)
    if not os.path.exists(file_path):
        return
    f = open(file_path, mode)
    content = f.read()
    f.close()
    return content


def parsePhone(content):
    '''
        解析手机号
    '''
    if content is None:
        return None
    re_phone = re.search(r'[1][3,4,5,6,7,8,9][0-9]{9}', content, re.S)
    phoneNum = None
    if re_phone:
        phoneNum = re_phone.group()
    return phoneNum


def parseNum(content):
    '''
        解析字符串中的数字
    '''
    if content is None:
        return None
    re_nums = re.findall(r'(\d+)', content, re.S)
    return re_nums


def checkPhone(content):
    '''
        校验是否是手机号
    '''
    phoneNum = parsePhone(content)
    if phoneNum is None:
        return False
    return True


def cnToNum(content):
    '''
        中文数字转英文
    '''
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
    content = content.replace(u"壹", "1")
    content = content.replace(u"贰", "2")
    content = content.replace(u"叁", "3")
    content = content.replace(u"肆", "4")
    content = content.replace(u"伍", "5")
    content = content.replace(u"陆", "6")
    content = content.replace(u"柒", "7")
    content = content.replace(u"捌", "8")
    content = content.replace(u"玖", "9")
    return content


def sleep(sSeconds, eSeconds, content=''):
    '''
        随机延迟
    '''
    if sSeconds > eSeconds:
        return
    sleep_time = random.uniform(sSeconds, eSeconds)
    sleep_time = round(sleep_time, 3)
    print(u'%s随机延迟时间:%s秒' % (content, sleep_time))
    time.sleep(sleep_time)


def sleep_time(sleep_time, content=''):
    '''
        延迟
    '''
    print(u'%s延迟时间:%s秒' % (content, sleep_time))
    time.sleep(sleep_time)


def sleep_hour(interval, content=''):
    second = interval * 60 * 60
    print(u'%s延迟时间:%s小时' % (content, interval))
    time.sleep(second)


def sleep_hour_random(s_interval, e_interval, content=''):
    '''
        延随机延迟小时
    '''
    interval = random.uniform(s_interval, e_interval)
    interval = round(interval)
    print(u'%s延迟时间:%s小时' % (content, interval))
    time.sleep(interval * 60 * 60)


def sleep_minute(interval, content=''):
    second = interval * 60
    print(u'%s延迟时间:%s分钟' % (content, interval))
    time.sleep(second)


def sleep_minute_random(s_interval, e_interval, content=''):
    interval = random.uniform(s_interval, e_interval)
    interval = round(interval)
    print(u'%s延迟时间:%s分钟' % (content, interval))
    time.sleep(interval * 60)


def md5(content):
    '''
        md5加密
        * 'content' 明文字符串
    '''
    if not isinstance(content, str):
        return
    m = hashlib.md5()
    m.update(content)
    return m.hexdigest()


def get_sign(parames):
    '''
        请求参数签名加密
        * 'parames' 参数字典
    '''
    if parames is None:
        return
    if not isinstance(parames, dict):
        return
    values = []
    for key, val in parames.items():
        values.append(str(val))
    values.sort()
    values_str = ','.join(values)
    return md5(values_str + "_sflyq")


def print_partition(content):
    '''
        分割线
        'content' 分割线中间内容
    '''
    print('')
    print('****************************************')
    print(content, time.strftime("%Y-%m-%d %H:%M:%S"))
    print('****************************************')
    print('')


def time_add_days(numbers):
    '''
        当前时间+n天
    '''
    now = datetime.datetime.now().date()
    date = now + datetime.timedelta(days=numbers)
    return date


def time_stamp():
    '''
        获取时间戳
    '''
    return int(time.time())


def time_now_str(style='%Y-%m-%d %H:%M:%S'):
    '''
        获取当前时间
    '''
    return time.strftime(style)


def get_time_str(time_stamp):
    '''
        根据时间戳获取时间字符串
    '''
    time_tuple = get_time_tuple(time_stamp)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)
    print(time_str)


def get_time_tuple(time_stamp):
    '''
        根据时间戳获取时间元组
    '''
    time_tuple = time.localtime(time_stamp)
    return time_tuple


def show_excute_start_time(func):
    '''
        装饰器：显示开始执行时间
    '''

    @functools.wraps(func)
    def show_time(*agrs, **kw):
        print(u'执行时间:%s' % time_now_str())
        return func(*agrs, **kw)

    return show_time


def show_segmentation_line(func):
    '''
        装饰器：显示分割线
    '''

    @functools.wraps(func)
    def segmentation_line(*agrs, **kw):
        print('')
        print(u'-------------------------------------------------')
        return func(*agrs, **kw)

    return segmentation_line


def url_query(url):
    '''
        解析url获取参数的字典
    '''
    if url is None:
        return {}
    query = urllib.parse.urlparse(url).query
    return dict([(k, v[0]) for k, v in urllib.parse.parse_qs(query).items()])


def path_absolute(dir=''):
    '''
        获取绝对路径
    '''
    dir_path = os.path.split(os.path.realpath(__file__))[0]
    if dir is not None and dir != '':
        dir_path = u'%s/%s' % (dir_path, dir)
    return dir_path


def excute_time(title):
    '''
        方法执行时间装饰器
    '''

    def fn_timer(func):
        @functools.wraps(func)
        def function_timer(*args, **kwargs):
            t0 = time.time()
            result = func(*args, **kwargs)
            t1 = time.time()
            print("Total time running %s: %s seconds" % (title, str(t1 - t0)))
            return result

        return function_timer

    return fn_timer


def zip_file(file_dir, save_dir, filename, mode='a'):
    '''
        文件zip压缩
        * 'file_dir' 需要压缩的文件路径
        * 'save_dir' 压缩文件的存储路径
        * 'filename' 压缩文件的文件名
        * 'mode' zip 操作文件的mode类型
    '''
    if not os.path.exists(file_dir):
        return False, u'zip_file=>file_dir=\'%s\'文件路径不存在' % file_dir
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # zip文件地址
    zip_file_path = u'%s/%s.zip' % (save_dir, filename)
    # 如果存在zip先删除
    if os.path.exists(zip_file_path):
        os.remove(zip_file_path)
    # zip压缩
    z = zipfile.ZipFile(zip_file_path, mode, zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(file_dir):
        for filename in filenames:
            z.write('%s/%s' % (file_dir, filename), filename)
            # print(u'%s' % filename)
    z.close()
    return True, None


def remove_emoji(text):
    '''
        过滤emoji表情符号
    '''
    emoji_pattern = re.compile(
        u"(\ud83d[\ude00-\ude4f])|"  # emoticons
        u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
        u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
        u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
        u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
        "+",
        flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def go_handle(snum, enum, handle_fn):
    '''
        构建上报数据，并上报存储
    '''
    if snum > enum:
        print(u'sum不能大于enum')
        return

    for num in range(snum, enum + 1):
        handle_fn(num)


def thread_handle(snum, enum, section, handle_fn):
    '''
        多线程处理
    '''
    threads = []
    while snum < enum:
        end = snum + section
        if end > enum:
            end = enum
        t = threading.Thread(target=go_handle, args=(snum, end, handle_fn))
        print(u'添加线程处理区间:%s-%s' % (snum, end))
        threads.append(t)
        snum = end
    print("go")
    for t in threads:
        t.setDaemon(True)
        t.start()
    # 等待所有线程完成
    for t in threads:
        t.join()
    print('over')


def re_search(pattern, content):
    '''
        正则查询
    '''
    if content is None:
        return None
    re_target = re.search(pattern, content, re.S)
    return re_target


# print(u'iOS 模块详解—「Runtime面试、工作」看我就 🐒 了 ^_^.')
# print(parseNum(u'啊啊发发的1发3sd444fsd'))
# a = "123abc456"
# mobj = parseNum(a)
# print(mobj)
