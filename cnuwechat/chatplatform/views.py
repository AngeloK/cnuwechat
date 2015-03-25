# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
from lxml.etree import fromstring
from WechatMessage import WechatMsg
from .models import Student

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
	content = "hello"

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

def authenticate(username,password):
        user = Student.objects.get(stuID = username)
        if user.password == password:
            return True
        else:
            return False

@csrf_exempt
def login(request):
        try:
            if request.session['studentid']:
                return HttpResponse(u"你已经成功绑定")
        except:
            pass
        if request.method == 'POST':
            print request.body
            username = request.POST['studentid']
            password = request.POST['password']

            if authenticate(username,password):
                request.session['studentid'] = username            
                return HttpResponse(u'登陆成功')
            else:
                return HttpResponse(u'登录失败，请重试')
        else:
            return render(request,'login_form.html')
def search_balance(request):
        try:
            current_id = request.session['studentid']
            current_user = Student.objects.get(stuID = current_id)
            return HttpResponse("Balance:%s" %current_user.card_balance)
        except:
            return HttpResponse(u"请先绑定")

def logout(request):
        request.session['studentid'] = None
        return HttpResponse(u"解绑成功")
