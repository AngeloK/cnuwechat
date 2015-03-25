# -*- coding: utf-8 -*-

import MySQLdb
import httplib
import json
import time

class GetAccessTokenError(BaseException):
	pass

class AccessToken(object):

	appId = 'wx9ffbc86c2b137040'
	appsecret = '9499f2749b3908326972ce2ba4c29b9e'

	access_token = None
	expires_in = None

	status = 0
	errmsg = None

	def __init__(self, *args, **kwargs):
		super(AccessToken, self).__init__(*args, **kwargs)

		#normal id


	def get_access_token(self):

		host = 'api.weixin.qq.com'
		path = '/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' %(appId,appsecret)
		
		conn = httplib.HTTPSConnection(host)
		conn.request('GET',path)
		raw_data = conn.getresponse()
		result = json.loads(raw_data.read())

		try:
			access_token = result['access_token']
			expires_in = result['expires_in']
			creat_at = time.time()
			print "Get access_token successfully"
		except:
			status = result['errcode']
			errmsg = result['errmsg']
			print "Get access_token failed"

class TokenPusher(AccessToken):

	def __init__(self, *args, **kwargs):
		super(AccessToken, self).__init__(*args, **kwargs)

	def push_to_database(self):
		

		


