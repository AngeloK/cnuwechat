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

    def get_chemistry_news():
        pass

    def get_biology_news():
        pass

    def get_info_engineer_news():
        index_url = 'http://www.ie.cnu.edu.cn/2011/index.php/Infodetail/shownotice'
        pass


        
    



