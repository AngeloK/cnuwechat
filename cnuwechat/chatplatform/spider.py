# CnuSpider.py
# coding=utf-8
import requests
from django.core.cache import cache
import urllib2
from bs4 import BeautifulSoup

class ArticleSpider(object):

    
    #def __init__(self):

        #self.title = []
        #self.description = []

    
    
    
    def get_school_news(self):
        #try:
            #news = cache.get('lastest')
            #print 'this executed!'
            #return news
        #except:
            

        url = 'http://www.cnu.edu.cn/xyxx/xygg/index.htm'
        url_head = 'http://www.cnu.edu.cn/xyxx/xygg/'
        res = urllib2.urlopen(url).read()
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
       
        return data

    def get_department_news(departmentId):
        pass


