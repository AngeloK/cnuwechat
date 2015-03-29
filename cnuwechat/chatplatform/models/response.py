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

class Responser(object):

    
    #def __init__(self,**kwrgs):

        #ins_code = kwrgs['content']

        #return ins_code

        
    def identify_data(self,d):

        is_pic_text_msg = True

        if d['MsgType']=='event':
            if d['Event'] == 'subscribe':
                content = u'欢迎关注首都师范大学微信公众平台教务信息自助查询系统，你的支持是我们最大的动力！'
                is_pic_text_msg = False
            elif d['Event'] == 'CLICK':
                spider = ArticleSpider()
                if d['EventKey'] == 'SCHOOL_NEWS':
                    content = spider.get_school_news()
                elif d['EventKey'] == 'DEPARTMENT_NEWS':
                    content = spider.get_math_news()
                else:
                    pass
            else:
                pass
        else:
            content = u'我正在锻炼自己有更好的交流功能，现在还很害羞^_^'
            is_pic_text_msg = False
        return content,is_pic_text_msg
        
    #def identify_data(self):

        #spider = ArticleSpider()
        #return spider.get_math_news()
        
                 

