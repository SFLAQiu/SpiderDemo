# coding:utf-8
import os
import re
import random
import time
import hashlib
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
    file_path = '%s\\%s' % (path, file_name)
    f = open(file_path, mode)
    f.write(content.encode("utf-8"))
    f.close()


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
    return content


def sleep(sSeconds, eSeconds, content=''):
    '''
        延迟
    '''
    if sSeconds > eSeconds:
        return
    sleep_time = random.uniform(sSeconds, eSeconds)
    sleep_time = round(sleep_time, 3)
    print u'%s随机延迟时间:%s秒' % (content, sleep_time)
    time.sleep(sleep_time)


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
    print ''
    print u'********************%s[%s]********************' % (
        content, time.strftime("%Y-%m-%d %H:%M:%S"))
    print ''


def time_stamp():
    '''
        获取时间戳
    '''
    return int(time.time())


def get_time_str(time_stamp):
    '''
        根据时间戳获取时间字符串
    '''
    time_tuple = get_time_tuple(time_stamp)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)
    print time_str


def get_time_tuple(time_stamp):
    '''
        根据时间戳获取时间元组
    '''
    time_tuple = time.localtime(time_stamp)
    return time_tuple