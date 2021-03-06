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

        departmentid = ['1','2','3','4','5','6','7']

        msgType = 'text'                        #Default message type is text
        content = ''

        if d['MsgType']=='event':
            if d['Event'] == 'subscribe':
                content = u'欢迎关注首都师范大学微信公众平台教务信息自助查询系统，你的支持是我们最大的动力！'
            elif d['Event'] == 'CLICK':
                spider = ArticleSpider()
                if d['EventKey'] == 'SCHOOL_NEWS':
                    msgType = 'pic_text'
                    content = spider.get_school_news()
                elif d['EventKey'] == 'DEPARTMENT_NEWS':
                    content = u'请回复对应数字查看详情\n[1]数学科学院\n[2]物理系\n[3]化学系\n[4]生命科学院\n[5]信息工程学院'
                elif d['EventKey'] == 'BALANCE_KEY':
                    openid = d['FromUserName']
                    balance = cache.get(openid)
                    if balance:
                        content = balance
                    else:
                        content = get_balance_str(openid)
                elif d['EventKey'] == 'BIND':
                    openid = d['FromUserName']
                    if cache.get(openid+'_cookie'):
                        content = push_login_link(openid,True)
                    else:
                        content = push_login_link(openid,False)
                elif d['EventKey'] == 'SCHEDULE':
                    content = u'功能能正在完善中，敬请期待'
            else:
                pass
        else:
            if d['Content'] in departmentid:
                spider = ArticleSpider()
                msgType = 'pic_text'
                content = spider.get_news_by_departmentid(d['Content'])
            else:
                content = u'我正在锻炼自己有更好的交流功能，现在还很害羞^_^'
        return content,msgType

def push_login_link(openid,is_user_stored):
    if is_user_stored:
        link_html = u'你已成功绑定'
    else:
        url = 'http://123.57.216.14/login?openid=%s' %openid
        link_html = u'若要启动查询功能<a href="%s">请先绑定</a>' %url
    return link_html

        

