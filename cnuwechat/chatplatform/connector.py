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
    
    
    def _create_cookie(self):
        cookie = dict(JSESSIONID=self._jsessionid,iPlanetDirectoryPro=self._iplanetdirectorypro)
        return cookie
        

    def authenticate(self):
        index_url = 'http://uid.cnu.edu.cn'
        login_url = 'http://uid.cnu.edu.cn/userPasswordValidate.portal'

        goto = 'http://uid.cnu.edu.cn/loginSuccess.portal'
        gotoOnFail = 'http://uid.cnu.edu.cn/loginFailure.portal'

        data = {'Login.Token1':self._username,'Login.Token2':self._password,'goto':goto,'gotoOnFail':gotoOnFail}
        
        index_cookie = requests.get(index_url).cookies 
        self._jsessionid = index_cookie['JSESSIONID']
        #self._safe_dog_flow = index_cookie['safedog_flow_item']
        login_response = requests.post(login_url,data,cookies=index_cookie)
        if login_response.status_code == 200:
            self._iplanetdirectorypro = login_response.cookies['iPlanetDirectoryPro']
            user_info = dict(JSESSIONID=self._jsessionid,iPlanetDirectoryPro=self._iplanetdirectorypro)
            cache.set(self._username,user_info,timeout=600)
            self.status = 1
        else:
            self.status = -1
        
    #def connect(self):
        #index_url = 'http://uid.cnu.edu.cn/index.portal'
        #if self.status:
            #cookie = self._create_cookie()
            #response = requests.get(index_url,cookies = cookie)
        #else:
            #error_msg = 'Error,username & password invalid or authenticat first'
            #print error_msg
            #return None

    def login_grade_system(self):
        grade_system_url = 'http://xk.cnu.edu.cn/zdtj.jsp'

        inner_login_url = 'http://xk.cnu.edu.cn/loginAction.do'

        iPlanetDirectoryPro = self._iplanetdirectorypro

        cookie = dict(iPlanetDirectoryPro=iPlanetDirectoryPro)
        
        res = requests.get(grade_system_url,cookies=cookie)

        self._jsessionid_inner = res.cookies['JSESSIONID']

        grade_system_cookie = dict(JSESSIONID=self._jsessionid_inner,iPlanetDirectoryPro=iPlanetDirectoryPro)
        
        
        

    def get_balance(self):

        user_info = cache.get(self._username)

        if user_info:
            try:
                return user_info['balance']
            except:
                pass
        
        index_url = 'http://uid.cnu.edu.cn/index.portal'

        if self.status == 1:
            cookie = self._create_cookie()

            res = requests.get(index_url,cookies=cookie)

            soup = BeautifulSoup(res.text)

     
            flow_head = u'校园网服务:\n'
            card_head = u'\n校园卡余额:'

            flow_balance = soup.find_all('div',class_='showdesc')

            for item in flow_balance[0].stripped_strings:
                flow_head = flow_head+' '+item


            card_block = soup.find_all('div',id='pf46')
            
            card_portletContent = card_block[0].find_all('div',class_='portletContent')[0]
            
            card_balance_div = card_portletContent.find('div')

            card_balance = card_balance_div.find('span').string
            
            card_head = card_head +card_balance + u'元'

            balance_result = flow_head + card_head
            
            user_info['balance'] = balance_result

            cache.set(self._username,user_info,timeout=600)
           
            return balance_result
        
        else:
            error_msg = u'请先绑定'
            return error_msg

        
