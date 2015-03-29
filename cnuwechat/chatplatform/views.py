# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import hashlib
from receiver import WechatMsg
from .models.eduModels import Student
from .models.eduModels import Schedule
from .forms import LoginForm
import datetime
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

    data = msg.parseToJson(msg_from_wechat)

    # content = contentResponse(data)
    # return HttpResponse(content)

    #content = "hello"
    picurl = 'http://365jia.cn/uploads/13/0301/5130c2ff93618.jpg'
    url = 'http://www.baidu.com'
    content1 = {'1':{'title':u'你好','description':u'文章描述','picurl':picurl,'url':url},'2':{'title':u'你好','description':u'文章描述','picurl':picurl,'url':url}}
    #transText = msg.build_text_msg(data,content)
    pic_transText = msg.build_picText_msg(data,content1)
    print pic_transText
    return HttpResponse(pic_transText)


@csrf_exempt
def main(request):
    if request.method == 'GET':
            try:
                return checkSignture(request)
            except:
                return index(request)
    elif request.method == 'POST':
            return receiveMsg(request)
    else:
            return Http404

def index(request):
    return render(request,'index.html')

def authenticate(username,password):
    '''
    authenticate username & password with them save in database
    '''
    user = Student.objects.get(stuID = username)
    if user.password == password:
        return True
    else:
        return False

@csrf_exempt
def login(request):
    '''
    After getting "post" requset,server authenticate username and password retrieved
    if user login successfully, a sessionID save, if this user enter login/ page the 
    second time, he will autumatically enter index/ page.
    '''
    if request.method == 'POST':
        try: 
            username = request.POST['studentid'] 
            password = request.POST['password'] 
            if authenticate(username,password):
                request.session['studentid'] = username
                messages.success(request,u'登陆成功，请返回')
                return redirect('index')
            else:
                pass
        except:
            messages.error(request,u'请输入正确的用户名和密码')
            return redirect('login')

    else:
        try:
            current_id = request.session['studentid']
            return render(request,'logout.html')
        except:
            form = LoginForm()
            return render(request,'login.html',{'form':form})

def search_balance(request):
    try:
        current_id = request.session['studentid']
        current_user = Student.objects.get(stuID = current_id)
        return render(request,'search.html',{'current_user':current_user,'department':current_user.departmentID})
    except:
        messages.info(request,u'请先绑定')
        return redirect('login')

def schedule(request):
    try:
        current_id = request.session['studentid']
        week_today = datetime.date.today().strftime('%w')
        current_schedule = Schedule.objects.filter(studentID_id = current_id).order_by('week')

        return render(request,'today_schedule.html',{'schedules':current_schedule})
    except:
        return HttpResponse(u"请先绑定")
        pass
    return render(request,'today_schedule.html')

def logout(request):
    try:
        del request.session['studentid']
    except KeyError:
        pass
    messages.info(request,u'解绑成功，请返回')
    return redirect('index')

def school_news(request):
    pass
