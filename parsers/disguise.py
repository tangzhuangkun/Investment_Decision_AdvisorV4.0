#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Tang Zhuangkun

import requests
import json
import time

import sys
sys.path.append("..")
import database.db_operator as db_operator
import log.custom_logger as custom_logger
import conf

class Disguise:
	# 获取代理IP和头文件 以隐匿
	# 提供两种方法，从数据库中获取一个IP和一个UA  或者 从数据库中获取多个IP和多个UA
	
	def __init__(self):
		pass
	
	def get_one_IP_UA(self):
		'''
		从数据库中获取一个UA
		从API获取一个代理IP
		:return:  1个IP和1个UA
		返回例如：({'ip_address': '183.164.244.236:18220'}, {'ua': 'Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'})
		'''
		try:
			# 从API获取代理IP
			response = requests.get(
				"https://proxy.qg.net/allocate?Key="+conf.proxyIPUsername+"&Num=1&AreaId=&DataFormat=json&DataSeparator=&Detail=0",
				timeout=1)
			# json格式解码
			data_json = json.loads(response.text)
			# 成功返回，但返回中的内容不可用
			if(data_json["Code"]!=0):
				# 日志记录
				msg = "IP代理接口返回失败代码 " + str(data_json["Code"])
				custom_logger.CustomLogger().log_writter(msg, lev='warning')
				return {'ip_address': None}, {'ua': None}
			# # 成功返回
			else:
				# 获取到的代理IP+代理端口
				ipAndPort = data_json["Data"][0]["host"]
				ip_address = {"ip_address":ipAndPort}
		except Exception as e:
			# 日志记录
			msg = "调用IP代理接口失败 " + str(e)
			custom_logger.CustomLogger().log_writter(msg, lev='warning')
			return self.get_one_IP_UA()

		# 获取UA
		ua_sql = "SELECT ua FROM fake_user_agent ORDER BY RAND() LIMIT 1"
		ua = db_operator.DBOperator().select_one('parser_component',ua_sql)
		
		return ip_address,ua
		
		
		
	def get_multi_IP_UA(self,num):
		'''
		从数据库中获取多个UA
		从API获取多个代理IP
		:param num: 需要多少个IP和UA
		:return: 多个IP和多个UA
		返回例如：([{'ip_address': '27.158.237.107:24135'}, {'ip_address': '27.151.158.219:50269'}], [{'ua': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36'}, {'ua': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6'}])
		'''

		ip_address_dict_list = list()

		try:
			# 从API获取代理IP
			response = requests.get(
				"https://proxy.qg.net/allocate?Key=" + conf.proxyIPUsername + "&Num="+str(num)+
				"&AreaId=&DataFormat=json&DataSeparator=&Detail=0",timeout=1)
			# json格式解码
			data_json = json.loads(response.text)
			# 成功返回，但返回中的内容不可用
			if (data_json["Code"] != 0):
				# 日志记录
				msg = "IP代理接口返回失败代码 " + str(data_json["Code"])
				custom_logger.CustomLogger().log_writter(msg, lev='warning')
				return [{'ip_address': None}], [{'ua': None}]
			# 成功返回
			else:
				data_list =data_json["Data"]
				for unit in data_list:
					# 获取到的代理IP+代理端口
					ipAndPort = unit["host"]
					ip_address = {"ip_address": ipAndPort}
					# 添加进返回中
					ip_address_dict_list.append(ip_address)
		except Exception as e:
			# 日志记录
			msg = "调用IP代理接口失败 " + str(e)
			custom_logger.CustomLogger().log_writter(msg, lev='warning')
			return self.get_one_IP_UA()
		
		# 获取多个UA
		ua_sql = "SELECT ua FROM fake_user_agent LIMIT %s" %(str(num))
		ua_dict_list = db_operator.DBOperator().select_all('parser_component',ua_sql)
		
		return ip_address_dict_list,ua_dict_list


if __name__ == "__main__":
	time_start = time.time()
	go = Disguise()
	result =go.get_multi_IP_UA(2)
	#result = go.get_one_IP_UA()
	print(result)
	time_end = time.time()
	print('time:')
	print(time_end - time_start)
		