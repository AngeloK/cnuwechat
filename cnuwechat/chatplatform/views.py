# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
import hashlib
from receiver import WechatMsg
from .models.eduModels import Student
from .models.eduModels import Schedule
from .models.response import Responser
from .forms import LoginForm
import datetime
from spider import ArticleSpider
from connector import CnuConnector
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
    msg = WechatMsg()
    msg_from_wechat = request.body

    j_data = msg.parseToJson(msg_from_wechat)

    respon = Responser()
    content,msgType = respon.identify_data(j_data)
    
    if msgType == 'text':
        transText = msg.build_text_msg(j_data,content)
    else:
        transText = msg.build_picText_msg(j_data,content)

    return HttpResponse(transText)

    
@csrf_exempt
def main(request):
    print cache.get('access_token')
    if request.method == 'GET':
            try:
                return checkSignture(request)
            except:
                return index(request)
    elif request.method == 'POST':
            return receiveMsg(request)
    else:
            return Http404('page not found')

def index(request):
    return render(request,'index.html')


@csrf_exempt
def login(request):

    if request.method == 'POST':
        username = request.POST['studentid']
        password = request.POST['password']
        openid = request.POST['openid']
        current_user = CnuConnector(username,password)

        current_user.authenticate(openid)

        if current_user.status == 1:
            messages.success(request,u'绑定成功，请返回')
            return redirect('index')
    else:
        openid = request.GET['openid']
        form = LoginForm()
        return render(request,'login.html',{'form':form,'openid':openid})

def schedule(request):
    return render(request,'today_schedule.html',{'schedules':current_schedule})

def logout(request):
    pass
    #try:
        #del request.session['studentid']
        #messages.info(request,u'解绑成功，请返回')
    #except KeyError:
        #pass
    #return redirect('index') 

def school_news(request):
    pass
