# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.db import models
from ..receiver import WechatMsg 
from ..spider import ArticleSpider

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

    
    def __unicode__(self):
        return self.openid


class Responser(object):

    
    #def __init__(self,**kwrgs):

        #ins_code = kwrgs['content']

        #return ins_code

        
    def identify_data(self,d):

        msgType = ''

        if d['MsgType']=='event':
            if d['Event'] == 'subscribe':
                content = u'欢迎关注首都师范大学微信公众平台教务信息自助查询系统，你的支持是我们最大的动力！'
                msgType = 'subcribe'
            elif d['Event'] == 'CLICK':
                spider = ArticleSpider()
                if d['EventKey'] == 'SCHOOL_NEWS':
                    msgType = 'news'
                    content = spider.get_school_news()
                elif d['EventKey'] == 'DEPARTMENT_NEWS':
                    content = spider.get_math_news()
                    msgType = 'news'
                elif d['EventKey'] == 'BALANCE_KEY':
                    msgType = 'balance'
                    content = None         #this type of content shoud authenticate first
                else:
                    pass
            else:
                pass
        else:
            msgType = 'text'
            content = u'我正在锻炼自己有更好的交流功能，现在还很害羞^_^'
        return content,msgType
        
    #def identify_data(self):

        #spider = ArticleSpider()
        #return spider.get_math_news()
        
                 

