# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import hashlib
from lxml.etree import fromstring
from WechatMessage import WechatMsg
from .models import Student
from .forms import LoginForm
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

def index(request):
    return render(request,'index.html')

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
                messages.info(request,u'您已绑定，请返回')
                return redirect('index')
        except:
            pass
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                try:
                    username = request.POST['studentid'] 
                    password = request.POST['password'] 
                except:
                    messages.error(request,u'学号不存在')
                    return redirect('login')
                if authenticate(username,password):
                    messages.success(request,u'登陆成功')
                    return redirect('index')
            else:
                messages.error(request,u'请输入正确的学号和密码')
                return redirect('login')
        else:
            form = LoginForm()
            return render(request,'login.html',{'form':form})
def search_balance(request):
        try:
            current_id = request.session['studentid']
            current_user = Student.objects.get(stuID = current_id)
            return HttpResponse("Balance:%s" %current_user.card_balance)
        except:
            return HttpResponse(u"请先绑定")

def logout(request):
    try:
        if request.session['studentid']: 
            request.server['studentid']=None
            messages.info(request,u'解绑成功')
        return redirect('index')
    except:
        messages.info(request,u'未绑定')
        return redirect('index')
