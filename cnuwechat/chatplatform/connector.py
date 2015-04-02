# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from django.core.cache import cache

class CnuConnector(object):


    def __init__(self,username,password):
        
        self._username = username
        self._password = password
        self._jsessionid = None
        self._jsessionid_inner = None
        self._iplanetdirectorypro = None
        self._safe_dog_flow = None
        self._ldap = None
        self._inner_password = None
        self.status = 0
        self.openid = None
    
    
    def create_cookie(self):
        cookie = dict(JSESSIONID=self._jsessionid,iPlanetDirectoryPro=self._iplanetdirectorypro)
        return cookie
        

    def authenticate(self,openid):
        index_url = 'http://uid.cnu.edu.cn'
        login_url = 'http://uid.cnu.edu.cn/userPasswordValidate.portal'

        goto = 'http://uid.cnu.edu.cn/loginSuccess.portal'
        gotoOnFail = 'http://uid.cnu.edu.cn/loginFailure.portal'

        data = {'Login.Token1':self._username,'Login.Token2':self._password,'goto':goto,'gotoOnFail':gotoOnFail}
        
        index_cookie = requests.get(index_url).cookies 
        self._jsessionid = index_cookie['JSESSIONID']
        login_response = requests.post(login_url,data,cookies=index_cookie)
        if login_response.status_code == 200:
            self._iplanetdirectorypro = login_response.cookies['iPlanetDirectoryPro']
            #user_info = dict(JSESSIONID=self._jsessionid,iPlanetDirectoryPro=self._iplanetdirectorypro)
            user_cookie = self.create_cookie()
            self.status = 1
            cache.set(openid+'_cookie',user_cookie,timeout=1000)
        else:
            self.status = -1

                

    def login_grade_system(self):
        grade_system_url = 'http://xk.cnu.edu.cn/zdtj.jsp'

        inner_login_url = 'http://xk.cnu.edu.cn/loginAction.do'

        iPlanetDirectoryPro = self._iplanetdirectorypro

        cookie = dict(iPlanetDirectoryPro=iPlanetDirectoryPro)
        
        res = requests.get(grade_system_url,cookies=cookie)

        self._jsessionid_inner = res.cookies['JSESSIONID']

        grade_system_cookie = dict(JSESSIONID=self._jsessionid_inner,iPlanetDirectoryPro=iPlanetDirectoryPro)
        
        
        

def get_balance_str(openid):

    user_cookie = cache.get(openid+'_cookie')
    balance = cache.get(openid+'_balance')
    if balance:
        return balance

    if user_cookie:
        
        index_url = 'http://uid.cnu.edu.cn/index.portal'

        res = requests.get(index_url,cookies=user_cookie)

        soup = BeautifulSoup(res.text)

        #name_head = u'学号:'+username + '\n'

        flow_head = u'校园网服务:\n'
        card_head = u'\n校园卡余额:'

        flow_balance = soup.find_all('div',class_='showdesc')

        for item in flow_balance[0].stripped_strings:
            flow_head = flow_head+' '+item + '\n'


        card_block = soup.find_all('div',id='pf46')
        
        card_portletContent = card_block[0].find_all('div',class_='portletContent')[0]
        
        card_balance_div = card_portletContent.find('div')

        card_balance = card_balance_div.find('span').string
        
        card_head = card_head +card_balance + u'元'

        balance_result = flow_head + card_head
            
        cache.set(openid+'_balance',balance_result,timeout=1000)
       
        return balance_result
    else:
        balance_result = u'请先登录'
        return balance_result
    

def get_balance_json(username,cookie):
    pass
