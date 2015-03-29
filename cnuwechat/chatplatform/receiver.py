# -*- coding:utf-8 -*-
import time
from lxml import etree
from lxml.etree import CDATA
from lxml.etree import tostring
from lxml.etree import fromstring
from spider import ArticleSpider 

class WechatMsg(object):

    '''
    Initialize message received from wechat server by agruements
    '''

    def __init__(self,fromUserName=None,toUserName=None,
                createTime=None,msgType=None,
                content=None):
            self.fromUserName = fromUserName
            self.toUserName = toUserName
            self.createTime = str(int(time.time()))
            self.msgType = msgType
            self.content =content
    
    def parseToJson(self,raw_data):

        '''
        Parse xml receive from Wechat server to json message 
        '''
        data = fromstring(raw_data)

        tag_list = [item.tag for item in data]
        text_list = [item.text for item in data]

        result = dict(zip(tag_list,text_list))

        return result


    def build_text_msg(self,received_data,call_back_content):
        ''' 
        Build satified xml message byreceived_data 
        ''' 

        msg = etree.Element('xml')

        toUserElt = etree.SubElement(msg,'ToUserName')
        toUserElt.text = CDATA(received_data['FromUserName'])

        fromUserElt = etree.SubElement(msg,'FromUserName')
        fromUserElt.text = CDATA(received_data['ToUserName'])

        createTime = etree.SubElement(msg,'CreateTime')
        createTime.text = str(int(time.time()))

        msgType = etree.SubElement(msg,'MsgType')
        msgType.text = CDATA('text')

        content = etree.SubElement(msg,'Content')
        #content.text = CDATA(call_back_content)
        content.text = call_back_content

        str_xml = tostring(msg,encoding='utf-8')

        return str_xml

    def build_picText_msg(self,received_data,data):
        '''
        Build content with picture and plain cotext
        data represent json data structure, for example,
        {'1':{"title":"xxx","description":"xxxx","picUrl":"www.ccc.com/1.jpg","url":"www.xxx.com/index.html"},
         '2':....}
        '''

        msg = etree.Element('xml')

        toUserElt = etree.SubElement(msg,'ToUserName')
        toUserElt.text = CDATA(received_data['FromUserName'])

        fromUserElt = etree.SubElement(msg,'FromUserName')
        fromUserElt.text = CDATA(received_data['ToUserName'])

        createTime = etree.SubElement(msg,'CreateTime')
        createTime.text = str(int(time.time()))

        msgType = etree.SubElement(msg,'MsgType')
        msgType.text = CDATA('news')

        articleCount = etree.SubElement(msg,'ArticleCount')
        articleCount.text = str(len(data))
        
        articles = etree.SubElement(msg,'Articles')

        for arti_count in range(1,len(data)+1):
            item = etree.SubElement(articles,'item')

            title = etree.SubElement(item,'Title')
            #title.text = CDATA(data['item'+str(arti_count)]['title'])
            title.text = data['item'+str(arti_count)]['title']

            description = etree.SubElement(item,'Description')
            description.text = CDATA(data['item'+str(arti_count)]['description'])

            picurl = etree.SubElement(item,'PicUrl')
            picurl.text = CDATA(data['item'+str(arti_count)]['picurl'])

            url = etree.SubElement(item,'Url')
            url.text = CDATA(data['item'+str(arti_count)]['url'])

        str_xml = tostring(msg,encoding='utf-8')
        return str_xml

    #def build_text_data(ins_code,departmentId=None):

        #spider = ArticleSpider()
        
        #if ins_code == '1':
            #data = spider.get_school_news()
        #elif ins_code == '2':
            #data = spider.get_department_news(departmentId)
        #else:
            #data = WechatMsg.normal_response()
            #return data
        
        #return data



