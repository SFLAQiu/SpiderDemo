# coding:utf-8
'''
    作者：SFLYQ

    功能：
        抢饿了么大红包
    思路：
        抓包饿了么抢红包页面，得到领取红包接口(领取并返回当前已领取红包用户列表)
            分析出领取红包接口：http://restapi.ele.me/marketing/promotion/weixin/xx  xx=根据不同用户而变化
            post json请求接口上报数据，其中：红包标识，微信uionid，头像，名称，sign，需要根据红包和微信用户变化
        分享红包地址：
            https://h5.ele.me/hongbao/?from=singlemessage#hardware_id=&is_lucky_group=True&lucky_number=7&track_id=&platform=0&sn=xxxx&theme_id=111&device_id=
            group_sn=红包标识
            lucky_number=大红包楼层
        流程：
            1.输入红包地址，分析出红包标识和大红包楼层
            2.小号进入红包领取，然后监控跟踪红包列表，当下一个楼层就是大红包的时候，主号去进行领取红包操作
            3.递归操作，直到大红包已经被其他抢，或者已经被自己抢到为止
        注意：
            饿了么红包领取接口有请求时间限制，所以我这里进行了延迟3s
        可优化：
            代理IP绕过请求限制，去掉延迟请求，这样就可以快速抢到红包
    注释：
        例子中xxx的数据都是微信相关信息，可以通过抓包过去到自己微信相关信息
    申明：
        我分享的爬虫功能仅供学习参考，如果拿去私用所有产生的后果由使用者自己承担

    运行正常日志输出：
        红包地址:
        https://h5.ele.me/hongbao/?from=singlemessage#hardware_id=&is_lucky_group=True&lucky_number=7&track_id=&platform=0&sn=xxxx&theme_id=111&device_id=

        -------------------------------------------------
        饿了么红包【xxx】
        执行时间:2017-10-13 16:27:04
        当前已抢楼层总数:2,下一个抢红包楼层:3
        第1个,参与人:xxx,抢到金额:3
        第2个,参与人:xxx,抢到金额:2
        目标：拿下第7楼层，继续监控，伺机而动！
        请求红包详情延迟时间:3秒

        -------------------------------------------------
        饿了么红包【xxx】
        执行时间:2017-10-13 16:27:08
        当前已抢楼层总数:2,下一个抢红包楼层:3
        第1个,参与人:xxx,抢到金额:3
        第2个,参与人:xxx,抢到金额:2
        目标：拿下第7楼层，继续监控，伺机而动！
        请求红包详情延迟时间:3秒
'''
# coding:utf-8
import os
import sys
import json
dir_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(dir_path + "/..")
import common.request as rq
import common.helper as hp

# 主账号红包领取接口地址
__get_hongbao_url = 'http://restapi.ele.me/marketing/promotion/weixin/oEGLvjstpZQYptuG78YA2PWbvoYE'

# 小号红包领取接口地址
__get_hongbao_url_dh = 'http://restapi.ele.me/marketing/promotion/weixin/oEGLvjszaWgjreVFbi1qKzH7Kivw'

# 大红包位置
__big_num = None
# 红包标识
__group_sn = None
# 小号饿了数据
__ele_data_xh = None
# 主号饿了数据
__ele_data_dh = None


@hp.show_excute_start_time
def get_hongbao(url, ele_data):
    '''
        自动领取红包，并返回红包JSON数据
    '''
    try:
        html = rq.post_cookie(
            url,
            ele_data,
            cookie_file_name="ele",
            headers={'Content-Type': 'application/json'})
    except Exception, e:
        print e
        return
    hb_data = json.loads(html)
    return hb_data


@hp.show_segmentation_line
def go_run():
    '''
        go抢饿了么红包
    '''
    print u'饿了么红包【%s】' % __group_sn
    hb_json = get_hongbao(__get_hongbao_url, __ele_data_xh)
    if hb_json is None:
        print u'无红包数据'
        return
    promotion_records = hb_json['promotion_records']
    if promotion_records is None:
        print u'无红包领取记录'
        return
    # 输出楼层情况
    current_num = len(promotion_records)
    next_num = current_num + 1
    print u'当前已抢楼层总数:%s,下一个抢红包楼层:%s' % (current_num, next_num)
    # 校验是否还有大红包
    if next_num == __big_num:
        print u'有大红包了，快动手'
        hb_json = get_hongbao(url=__get_hongbao_url_dh, ele_data=__ele_data_dh)
        print u'已经出手'
        hp.sleep_time(3, u'领取红包')

    # 列出当前已经抢列表
    for index, item in enumerate(promotion_records):
        level = index + 1
        username = item['sns_username']
        amount = item['amount']
        print u'第%s个,参与人:%s,抢到金额:%s' % (level, username, amount)
        if level == __big_num and username == __ele_data_dh['weixin_username']:
            print u'bingo! 红包已经到手!'
            return
    # 校验是否还有大红包
    if next_num > __big_num:
        print u'失手了，再来个红包吧'
        return
    print u'目标：拿下第%s楼层，继续监控，伺机而动！' % __big_num
    # 延迟，以免被限制
    hp.sleep_time(3, u'请求红包详情')
    go_run()


def build_data(group_sn, sign, weixin_username, weixin_avatar, unionid):
    '''
        创建数据
    '''
    ele_data = {
        "method": "phone",
        "group_sn": group_sn,
        "sign": sign,
        "phone": "",
        "device_id": "",
        "hardware_id": "",
        "platform": 0,
        "track_id": "undefined",
        "weixin_avatar": weixin_avatar,
        "weixin_username": weixin_username,
        "unionid": unionid
    }
    return ele_data


def bulild():
    '''
        构造数据
    '''

    global __ele_data_xh, __ele_data_dh
    # 小号头像
    avatar_xh = 'http://wx.qlogo.cn/mmopen/vi_32/xxx/0'
    # 主号头像
    avatar_dh = 'http://wx.qlogo.cn/mmopen/vi_32/xxx/0'
    # 小号
    __ele_data_xh = build_data(__group_sn, 'xxx', u'xxx', avatar_xh, 'xx')
    # 主号
    __ele_data_dh = build_data(__group_sn, 'xxx', u'xxx', avatar_dh, 'xxx')


def init():
    '''
        初始化操作
    '''
    global __group_sn, __big_num
    hb_url = raw_input(u"红包地址:\r\n".encode('gb2312'))
    if hb_url is None or hb_url == '':
        print u'非法红包地址'
        return
    # 解析参数
    hb_url = hb_url.replace('#', '')
    url_query = hp.url_query(hb_url)
    __big_num = 0
    # 获取红包信息
    if url_query.has_key('sn'):
        __group_sn = url_query['sn']
    if url_query.has_key('lucky_number'):
        __big_num = url_query['lucky_number']
    # 校验红包信息合法性
    __big_num = int(__big_num)
    if __group_sn is None or __group_sn == '':
        print u'非法红包标识'
        return
    if __big_num is None or __big_num <= 0:
        print u'非法大红包楼层'
        return
    # 初始化构建数据
    bulild()
    # 跑红包监控
    go_run()


init()
