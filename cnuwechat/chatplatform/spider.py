# CnuSpider.py
# coding=utf-8
import requests as req
from django.core.cache import cache
from django.contrib import messages
from django.shortcuts import redirect
import urllib2
from bs4 import BeautifulSoup

class ArticleSpider(object):

    
    #def __init__(self):

        #self.title = []
        #self.description = []
    
    def get_balance(self,request):
        
        try:
            current_id = request.session['studentid']
            current_user = cache.get(current_id)
            
            if current_user:
                try:
                    balance = current_user['balance']
                    return balance
                except:
                    pass

            index_url = 'http://uid.cnu.edu.cn/index.portal'
            
            cookie = current_user['user_auth']

            res = req.get(index_url,cookies=cookie)

            soup = BeautifulSoup(res.text)

     
            flow_head = u'校园网服务\n'
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

            current_user['balance'] = balance_result

            cache.set(current_id,current_user,timeout=600)

            return balance_result
        except:
            content = u'请先绑定'
            return content


    def get_school_news(self):

        school_news = cache.get('school_news')

        if school_news:
            return school_news
        else:
            index_url = 'http://www.cnu.edu.cn/xyxx/xygg/index.htm'
            url_head = 'http://www.cnu.edu.cn/xyxx/xygg/'
            res = urllib2.urlopen(index_url).read()
            soup = BeautifulSoup(res)

            pg_list = soup.find_all('div',class_='pg_list')
            article_li = pg_list[0].find_all('li',limit=5)
            
            data = {}
            description = ''
            picurl = 'http://ico.ooopic.com/ajax/iconpng/?id=115767.png'
            item_index = 1
            for item in article_li:
                
                title = item.a['title']
                url = url_head+item.a['href']
                article = dict(title=title,url=url,description=description,picurl=picurl)
                data['item%d' %item_index] = article
                item_index = item_index + 1

            # link for search more '查看更多'
            title = u'查看更多'
            url = index_url
            article = dict(title=title,url=url,description=description,picurl=picurl)
            data['item%d' %(item_index)] = article

            cache.set('school_news',data,timeout=600)
            return data
        

    def get_math_news(self):

        math_news = cache.get('math_news')
        if math_news:
            return math_news
        else:
            index_url = 'http://202.204.208.109/mathpage/newscenter.aspx'
            url_head = 'http://202.204.208.109/mathpage/'
            
            res = urllib2.urlopen(index_url).read()
            soup = BeautifulSoup(res)

            pg_list = soup.find_all('table')

            article_li = pg_list[1].find_all('a',limit=5)

            data = {}
            description = ''
            picurl = 'http://ico.ooopic.com/ajax/iconpng/?id=115767.png'

            item_index = 1
            for item in article_li:
                titles = item.stripped_strings
                titles.next()
                titles.next()
                titles.next()
                title = titles.next()[6:]
                url = url_head+item['href']
                article = dict(title=title,url=url,description=description,picurl=picurl)
                data['item%d' %item_index] = article
                item_index = item_index + 1

            title = u'查看更多'
            url = index_url
            article = dict(title=title,url=url,description=description,picurl=picurl)
            data['item%d' %(item_index)] = article

            cache.set('math_news',data,timeout=600)

            return data

    def get_chemistry_news(self):

        chemistry_news = cache.get('chemistry_news')

        if chemistry_news:
            return chemistry_news
        
        index_url = 'http://202.204.208.109/hxx/index.php?q=xxgg'
        url_head = 'http://202.204.208.109/'
        
        res = urllib2.urlopen(index_url).read()
        soup = BeautifulSoup(res)

        art_div = soup.find_all('div',class_='views-field-title',limit=3)
      
        data = {}
        description = ''
        picurl = 'http://ico.ooopic.com/ajax/iconpng/?id=115767.png'
    
        item_index = 1
        for item in art_div:
            title = unicode(item.a.string)
            url = url_head+item.a['href']
            article = dict(title=title,url=url,description=description,picurl=picurl)
            data['item%d' %item_index] = article
            item_index = item_index + 1 

        title = u'查看更多'
        url = index_url
        article = dict(title=title,url=url,description=description,picurl=picurl)
        data['item%d' %(item_index)] = article

        cache.set('chemistry_news',data,timeout=600)


        return data

    def get_biology_news(self):

        school_news = cache.get('school_news')

        if school_news:
            return school_news
        else:
            index_url = 'http://smkxxy.cnu.edu.cn/tzgg/index.htm'
            url_head = 'http://smkxxy.cnu.edu.cn/tzgg/'
            res = urllib2.urlopen(index_url).read()
            soup = BeautifulSoup(res)

            pg_list = soup.find_all('div',class_='r_l_list02')
            article_li = pg_list[0].find_all('li',limit=5)
            
            data = {}
            description = ''
            picurl = 'http://ico.ooopic.com/ajax/iconpng/?id=115767.png'
            item_index = 1
            for item in article_li:
                
                title = item.a.string[12:]
                url = url_head+item.a['href']
                article = dict(title=title,url=url,description=description,picurl=picurl)
                data['item%d' %item_index] = article
                item_index = item_index + 1

            # link for search more '查看更多'
            title = u'查看更多'
            url = index_url
            article = dict(title=title,url=url,description=description,picurl=picurl)
            data['item%d' %(item_index)] = article

            cache.set('school_news',data,timeout=600)
            return data
        



    def get_info_engineering_news(self):

        info_engineering_news = cache.get('engineering_news')
        if info_engineering_news:
            return info_engineering_news
        index_url = 'http://www.ie.cnu.edu.cn/2011/index.php/Infodetail/shownotice'
        url_head = 'http://http://www.ie.cnu.edu.cn/2011/'
        res = urllib2.urlopen(index_url).read()
        soup = BeautifulSoup(res)
        at_list =soup.find('ul',class_='newsize')

        article_li = at_list.find_all('li',limit=5) 

        data = {}
        description = ''
        picurl = 'http://ico.ooopic.com/ajax/iconpng/?id=115767.png'
        item_index = 1
        for item in article_li:
            title = item.a.string[26:]
            url = url_head + item.a['href']
            article = dict(title=title,url=url,description=description,picurl=picurl)
            data['item%d' %item_index] = article
            item_index = item_index + 1

        title = u'查看更多'
        url = index_url
        article = dict(title=title,url=url,description=description,picurl=picurl)
        data['item%d' %(item_index)] = article
        cache.set('engineering_news',data,timeout=600)
        return data

    def get_physcis_news(self):
        pass

    def get_news_by_departmentid(self,departmentid):
       
        if departmentid == '1':
            return self.get_math_news()
        #if departmentid == '2':
            #return self.get_physcis_news()
        if departmentid == '3':
            return self.get_chemistry_news()
        if departmentid == '4':
            return self.get_biology_news()
        if departmentid == '5':
            return self.get_info_engineering_news()

        return -1 



