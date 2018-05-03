# coding:utf-8
'''
    作者：SFLYQ
    功能：
        58保险代理人工作信息爬取
    申明：
        我分享的爬虫功能仅供学习参考，如果拿去私用所有产生的后果由使用者自己承担
'''
import os
import sys
import re
import time
from pyquery import PyQuery as jquery
dir_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(dir_path + "/..")
import commons.request as rq
import commons.helper as hp
import json
import random
# 工作查询接口
__agencys_url = u'http://{}.58.com/job/pn{}/?key=%E4%BF%9D%E9%99%A9%E4%BB%A3%E7%90%86%E4%BA%BA&final=1&jump=1'
# 手机号图片地址
__phone_url = u'http://image.58.com/showphone.aspx?t=v55&v={}'
# 城市url
__city_url = u'http://www.58.com/changecity.html?fullpath=1'
# 城市
__citys = []
# 工作集合
__jobs = []


def get_agencys(city, page_index=1):
    '''
        获取58全职搜索保险代理人信息
        * 'city_type' 城市类型
        * 'page_index' 当前页码
    '''
    city_type = city['id']
    hp.print_partition(u'解析城市：%s-%s-%s,保险代理人的工作' % (city['province'],
                                                    city['city'], city['id']))
    # 构造接口url
    url = __agencys_url.format(city_type, page_index)
    print(u'工作地址：%s' % url)
    try:
        # html = rq.get_cookie(
        #     url,
        #     headers={
        #         "User-agent":
        #         "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        #         "Referer":
        #         url
        #     })
        html = rq.get(url)
    except Exception as e:
        print(e)
        return
    doc = jquery(html)
    if doc is None:
        print(u"解析html报错")
        return
    # 总页数
    page_nums_str = doc.find(".num_operate .total_page").html()
    if page_nums_str is None:
        page_nums_str = '0'
    page_nums = int(page_nums_str)
    print(u'总页数：%s，当前页码：%s' % (page_nums, page_index))
    # 工作列表
    list_jobs = doc.find("#list_con .job_item")
    if list_jobs is None:
        print(u"没有查询到工作列表信息")
        return
    print(u"工作总数:%s" % len(list_jobs))
    # 遍历工作
    today_nums = 0
    for job_item in list_jobs:
        job_item_jq = jquery(job_item)
        job_sign = job_item_jq.find(".sign").html()
        if not check_job_istoday(job_sign):
            print(u'状态：%s，不是今日发布，略过' % job_sign)
            continue
        today_nums = today_nums + 1
        job_name = job_item_jq.find(".name").html()
        if job_name.find(u'保险') < 0:
            print(u'工作：%s,非保险类工作，略过~' % job_name)
            continue
        job_address = job_item_jq.find(".address").html()
        job_url = job_item_jq.find("a").attr("href")
        job_company = job_item_jq.find(".job_comp .comp_name .fl").attr(
            "title")
        job_company = analysis_job_company(job_company)
        print(u'%s|%s|%s' % (job_address, job_name, job_sign))
        # 延迟
        hp.sleep(0.3, 0.6, content=u'获取工作详情=》')
        # 解析job_data数据
        job_data = analysis_job_data(job_url)

        if job_data is None or job_data['pagenum'] is None:
            print(u'无法获取pagenum，略过！')
            continue
        __jobs.append({
            "name": job_name,
            "address": job_address,
            "url": job_url,
            "pagenum": job_data['pagenum'],
            "contactPerson": job_data['contactPerson'],
            "sign": job_sign,
            "company": job_company
        })
    print(u'当前页码:%s,总页数：%s' % (page_index, page_nums))
    # 校验是否需要继续翻页
    if today_nums <= 0:
        print('当前页码:%s，无今日工作，无需继续翻页' % (page_index))
        return
    page_index = page_index + 1
    # 递归翻页
    if page_index <= page_nums:
        print(' ')
        # 延迟
        hp.sleep(0, 1, content=u'翻页=》')
        get_agencys(city, page_index)


def check_job_istoday(sign):
    '''
        校验是否今日发布
    '''
    if sign is None:
        return True
    if sign.find(u'精准') >= 0 or sign.find(u'优选') >= 0 or sign.find(u'今天') >= 0:
        return True
    return False


def analysis_job_data(job_url):
    '''
        解析job详情页面里的pagenum数据
    '''
    if job_url is None:
        print(u'工作详情地址为空，略过')
        return
    print('job_url=%s' % job_url)
    try:
        # html = rq.get_cookie(job_url, cookie_file_name=get_cookie_name())
        html = rq.get(job_url)
    except Exception as e:
        print(e)
        return
    # 解析工作标识
    pagenum = job_pagenum(html)
    # 解析工作联系人
    contactPerson = job_contactPerson(html)
    return {'pagenum': pagenum, 'contactPerson': contactPerson}


def analysis_job_company(company):
    '''
        获取公司名称
    '''
    if company is None:
        return u'未知'
    index = company.find(u'保险')
    if index < 0:
        return company
    company = company[0:index]
    company = company.replace('\\', '').replace('\/', '').replace(' ', '')
    return company


def job_pagenum(html):
    '''
        解析工作的pagenum(工作标识)
    '''
    sch = re.search(r'pagenum.?:"([^"]+?)",', html, re.S)
    if sch is None:
        print(u'无法解析pagenum')
        return
    pagenum = sch.groups()[0]
    print(u'解析出pagenum=%s' % pagenum)
    return pagenum


def job_contactPerson(html):
    '''
        解析工作的contactPerson(工作联系人)
    '''
    sch = re.search(r'contactPerson.?:.?"([^"]+?)"', html, re.S)
    if sch is None:
        print(u'无法解析contactPerson(工作联系人)')
        return
    contactPerson = sch.groups()[0]
    print(u'解析出contactPerson=%s' % contactPerson)
    return contactPerson


def download_phone(city):
    '''
        下载手机号图片
    '''
    hp.print_partition(u'下载手机号图片')
    print(u'获取到工作总数：%s' % len(__jobs))

    file_path = u"%s\\imgs\\58\\%s" % (dir_path, time.strftime("%Y-%m-%d"))
    for job in __jobs:
        print(job["name"], job["address"], job["contactPerson"])
        # 格式化工作信息
        job_contactPerson = u'未知' if job["contactPerson"] is None else job[
            "contactPerson"].replace(' ', '').replace('/', '-')
        job_city = city['city']
        job_province = city['province']
        job_company = job['company']
        # 下载手机号图片
        file_name = u'%s-%s-%s-%s' % (job_province, job_city,
                                      job_contactPerson, job_company)
        url = __phone_url.format(job["pagenum"])
        # 延迟
        hp.sleep(0.2, 0.5, content=u'下载=》')
        try:
            rq.down_image(
                url,
                file_path,
                file_name,
                cookie_file_name=get_cookie_name(),
                decode=None)
            print(u'下载完成')
        except Exception as e:
            print('下载失败原因：%s' % e)
    return


def get_citys():
    '''
        获取城市
    '''
    try:
        html = rq.get_cookie(__city_url)
    except Exception as e:
        print(e)
        return
    sch = re.search(r'var cityList.?=.?(\{[^<]+\})', html, re.S)
    if sch is None:
        print(u'无法解析cityList')
        return
    cityList_str = sch.groups()[0]
    cityList = json.loads(cityList_str)
    # 遍历省份
    for (province, citys) in cityList.items():
        # 遍历城市
        for (city, info) in citys.items():
            city_id = info.split('|')[0]
            # 添加城市信息
            print(province, city, city_id)
            __citys.append({"province": province, "city": city, "id": city_id})


def get_cookie_name():
    num = random.uniform(1, 20)
    return 'cookie_58_%s' % int(num)


def do_handle_init():

    print(u'获取城市')
    get_citys()
    for city in __citys:
        print(u'开始获取工作')
        get_agencys(city)
        print(u'开始下载手机号')
        download_phone(city)
        global __jobs
        __jobs = []


do_handle_init()
