from __future__ import absolute_import
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.cache import cache
import urllib2
from datetime import datetime
import json


logger = get_task_logger(__name__)

@shared_task
def get_access_token(appId,appsecret):
    
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' %(appId,appsecret)

    res = urllib2.urlopen(url)
    response = json.loads(res.read())
    now = datetime.now().strftime('%m-%d-%y,%H:%M:%S')
    as_token = response['access_token']
    result = '['+as_token+']'+'at'+now
    logger.info('current access_token will expire in 7000 from now(%s)' %now)
    cache.set('access_token',as_token,timeout=7200)
    return result
    

@shared_task
def store_jession_and_iplanet_in_cache():
    pass
    
