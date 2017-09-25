# coding:utf-8
import os
import re
import random
import time
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


def sleep(sSeconds, eSeconds):
    '''
        延迟
    '''
    if sSeconds > eSeconds:
        return
    sleep_time = random.uniform(sSeconds, eSeconds)
    sleep_time = round(sleep_time, 3)
    print u'随机延迟时间:%s秒' % sleep_time
    time.sleep(sleep_time)