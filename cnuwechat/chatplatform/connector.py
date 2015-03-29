# -*- coding:utf-8 -*-
import requests

class CnuConnector(object):


    def __init__(self,username,password):
        
        self._username = username
        self._password = password
        self._jsessionid = None
        self._iplanetdirectorypro = None
        self.status = 0

    def authenticate(self):
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
            self.status = 1
        else:
            self.status = -1
        
    def connect(self):
        if self.status:
            cookie = dict(JSESSIONID=self._jsessionid,iPlanetDirectoryPro=self._iplanetdirectorypro)
            response = requests.get(index_url,cookies = cookie)
            return response.text
        else:
            error_msg = 'Error,username & password invalid or authenticat first'
            print error_msg
            return None
