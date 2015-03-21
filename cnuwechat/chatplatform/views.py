# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
from lxml.etree import fromstring
from WechatMessage import WechatMsg


# Create your views here.

def checkSignture(request):
	'''
	Check signature 
	'''
	signature = request.GET['signature']
	timestamp = request.GET['timestamp']
	nonce = request.GET['nonce']
	echostr = request.GET['echostr']

	token = 'kangyongjie'

	sorted_str = sorted([token,timestamp,nonce])
	result_str = str(sorted_str[0]+sorted_str[1]+sorted_str[2])				

	result = hashlib.sha1(result_str).hexdigest()

	if signature and result == signature:
		return HttpResponse(echostr)
	else:
		return HttpResponse("not match")

def parseToJson(raw_data):

	'''
	Parse xml receive from Wechat server to json message 
	'''
	data = fromstring(raw_data)

	tag_list = [item.tag for item in data]
	text_list = [item.text for item in data]

	result = dict(zip(tag_list,text_list))

	return result

def receiveMsg(request):
	'''
	receive message from wechat server
	'''	
	msg_from_wechat = request.body

	data = parseToJson(msg_from_wechat)

	msg = WechatMsg()

	# content = contentResponse()
	content = '<a href="https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx04feb7b61454d11a&redirect_uri=http://123.57.216.14/oauth2/auth&response_type=code&scope=snsapi_userinfo&state=1#wechat_redirect">点击这里绑定</a>'

	transText = msg.build_text_msg(data,content)

	return HttpResponse(transText)


@csrf_exempt
def main(request):
	if request.method == 'GET':
		return checkSignture(request)
	elif request.method == 'POST':
		return receiveMsg(request)
	else:
		return Http404