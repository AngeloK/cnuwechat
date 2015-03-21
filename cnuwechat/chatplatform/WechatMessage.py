# -*- coding: utf-8 -*-
import time
from lxml import etree
from lxml.etree import CDATA
from lxml.etree import tostring 


class WechatMsg(object):

	'''
	Initialize message received from wechat server by agruements
	'''

	def __init__(self,
				fromUserName=None,
				toUserName=None,
				createTime=None,
				msgType=None,
				content=None):
		self.fromUserName = fromUserName
		self.toUserName = toUserName
		self.createTime = str(int(time.time()))
		self.msgType = msgType
		self.content =content



	def build_text_msg(self, received_data,call_back_content):

		''' 
		Build satified xml message byreceived_data 
		''' 
		# root = etree.Element('xml')
		# msg = etree.ElementTree(root)

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
		content.text = CDATA(call_back_content)

		xml_msg = tostring(msg)

		return xml_msg
