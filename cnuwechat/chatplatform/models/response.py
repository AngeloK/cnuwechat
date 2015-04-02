# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.db import models
from ..receiver import WechatMsg 
from ..spider import ArticleSpider
from ..connector import get_balance_str

class ContentResponse(models.Model):

    ins_code = models.CharField(max_length=50,unique=True)
    instruct = models.CharField(max_length=50)

    class Meta:
        app_label = 'chatplatform'

    def __unicode__(self):
        return self.ins_code

class CnuUser(models.Model):

    openid = models.CharField(max_length=100,unique=True)
    studentid = models.CharField(max_length=100,unique=True)
    jsessionid = models.CharField(max_length=100)
    iplanetdirectorypro = models.CharField(max_length=200)

    class Meta:
        app_label = 'chatplatform'
    def __unicode__(self):
        return self.openid


class Responser(object):

    
    #def __init__(self,**kwrgs):

        #ins_code = kwrgs['content']

        #return ins_code

        
    def identify_data(self,d):

        msgType = 'text'                        #Default message type is text

        if d['MsgType']=='event':
            if d['Event'] == 'subscribe':
                content = u'欢迎关注首都师范大学微信公众平台教务信息自助查询系统，你的支持是我们最大的动力！'
            elif d['Event'] == 'CLICK':
                spider = ArticleSpider()
                if d['EventKey'] == 'SCHOOL_NEWS':
                    msgType = 'pic_text'
                    content = spider.get_school_news()
                elif d['EventKey'] == 'DEPARTMENT_NEWS':
                    content = spider.get_math_news()
                    msgType = 'pic_text'
                elif d['EventKey'] == 'BALANCE_KEY':
                    openid = d['FromUserName']
                    balance = cache.get(openid)
                    if balance:
                        content = balance
                    else:
                        content = get_balance_str(openid)
                        print content
                elif d['EventKey'] == 'BIND':
                    openid = d['FromUserName']
                    if cache.get(openid+'_balance'):
                        content = push_login_link(openid,True)
                    else:
                        content = push_login_link(openid,False)
            else:
                pass
        else:
            content = u'我正在锻炼自己有更好的交流功能，现在还很害羞^_^'
        return content,msgType

def push_login_link(openid,is_user_stored):
    if is_user_stored:
        link_html = u'<p>你已成功绑定</p>'
    else:
        url = 'http://127.0.0.1:8000/login?openid=%s' %openid
        link_html = u'<p>若要启动查询功能<a href="%s">请先绑定</a></p>' %url
    return link_html

        

