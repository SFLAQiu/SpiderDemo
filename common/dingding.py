import commons.request as rq
import json


class helper(object):
    @staticmethod
    def inform(api, message):
        '''
            钉钉消息推送
        '''
        if not api:
            print(u'api地址不能为空')
            return
        if not message:
            message = ''
        try:
            data = {"msgtype": "text", "text": {"content": message}}
            rt = rq.post_cookie(
                api, data, headers={'Content-Type': 'application/json'})
            return json.loads(rt)
        except Exception as ex:
            print(u'请求钉钉报错:%s' % ex)
            return None

    @staticmethod
    def inform_markdown(api, title="", content=""):
        '''
            钉钉消息推送
        '''
        if not api:
            print(u'api地址不能为空')
            return
        if not title:
            title = "通知"
        try:
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": content
                }
            }
            rt = rq.post_cookie(
                api, data, headers={'Content-Type': 'application/json'})
            return json.loads(rt)
        except Exception as ex:
            print(u'请求钉钉报错:%s' % ex)
            return None
