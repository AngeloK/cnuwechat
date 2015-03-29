# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.db import models


class ContentResponse(models.Model):

    ins_code = models.CharField(max_length=50,unique=True)
    instruct = models.CharField(max_length=50)

    class Meta:
        app_label = 'chatplatform'

    def __unicode__(self):
        return self.ins_code

class Response(object):

    
    def __init__(self,**kwrgs):

        ins_code = kwrgs['content']

        return ins_code



    def build_receive_msg(ins_code):
        pass

        
