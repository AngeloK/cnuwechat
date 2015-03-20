# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
from lxml.etree import fromstring


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

def receiveMsg(request):
	'''
	receive message from wechat server
	'''

	data = fromstring(request.body)

	tag_list = [item.tag for item in data]
	text_list = [item.text for item in data]

	replyMsg = dict(zip(tag_list,text_list))

	response = HttpResponse(str(replyMsg))
	return response
@csrf_exempt
def main(request):

	if request.method == 'GET':
		return checkSignture(request)
	elif request.method == 'POST':
		return receiveMsg(request)
	else:
		return Http404