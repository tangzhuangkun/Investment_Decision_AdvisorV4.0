import urllib.request
import urllib.parse 
import socket
import re
import urllib.error
import bs4
import sys
sys.path.append('..')
import log.custom_logger as custom_logger

class ParseIPWebContent:
	def __init__(self):
		pass
	
	def parse_web_content(self,url):
		# url: IP代理网站的地址
		
		
		# 解析页面
		# 根据不同的网站名称，制定不同的解析提取规则
		# 输出：set(tuple(ip地址:端口号，匿名类型，协议类型) ---- set(tuple(ipAndPort,anonymous_type,protocol),,,)
		
		
		try:
			# 通过requests的get方法访问目标网站，超时限时 2秒
			f = urllib.request.urlopen(url,timeout=2)
			# 解析获得的响应对象
			# utf-8格式解码，
			# 解码的时候加上ignore参数是因为解码过程中有一部分貌似不能正常解码，加上该参数之后能跳过该部分
			raw_content = f.read().decode('utf-8','ignore')
			# 使用beautifulsoup 解析页面
			soup = bs4.BeautifulSoup(raw_content,'html.parser')
		except Exception as e:
			# print('Error:', e)
			# 日志记录
			msg = url + '  '+ str(e)
			custom_logger.CustomLogger().log_writter(msg)
			
		except urllib.error.URLError as e:
			if isinstance(e.reason, socket.timeout):
				# print('TIME OUT')
				# 日志记录
				
				msg = url + '  '+ 'TIME OUT'
				custom_logger.CustomLogger().log_writter(msg)
				
		
		# 通过url地址获取网站名称
		web_name = url.split('.')[1]
		
		# 储存当前解析页面的代理IP信息, 
		# set(tuple(ip地址:端口号，匿名类型，协议类型) ---- set(tuple(ipAndPort,anonymous_type,protocol),,,)
		page_proxy_ip_detail_set = set()
		
		
		if  web_name == 'kuaidaili' or web_name == 'xiladaili' or web_name == 'nimadaili':
			# 解析获取的HTML数据
			for tr_content in soup.find_all('tbody'):
				for td_content in tr_content.find_all('tr'):
					td_content_list = td_content.find_all('td')
					#print(td_content_list)
					
					if web_name == 'nimadaili':
						# 获取解析后的IP地址+端口号
						ipAndPort = td_content_list[0].get_text()
						# 获取解析后的协议类型
						protocol = td_content_list[1].get_text()[:-2]
						# 获取解析后的匿名类型
						anonymous_type = td_content_list[2].get_text()
					
						page_proxy_ip_detail_set.add((ipAndPort,anonymous_type,protocol))
						
					elif web_name == 'kuaidaili':
				
						# 获取解析后的IP地址
						ip = td_content_list[0].get_text()
						# 获取解析后的端口号
						port = td_content_list[1].get_text()
						# 获取解析后的匿名类型
						anonymous_type = td_content_list[2].get_text()
						# 获取解析后的协议类型
						protocol = td_content_list[3].get_text()
						# 拼接IP地址+端口号
						ipAndPort = ip+':'+port
					
						page_proxy_ip_detail_set.add((ipAndPort,anonymous_type,protocol))
						
			return page_proxy_ip_detail_set           
		
		elif web_name == 'yqie':
			# 解析获取的HTML数据
			for tr_content in soup.find_all('body'):
				for td_content in tr_content.find_all('tr'):
					if td_content.find('td'):
						td_content_list = td_content.find_all('td')     
						
						# 获取解析后的IP地址
						ip = td_content_list[1].get_text()
						# 获取解析后的端口号
						port = td_content_list[2].get_text()
						# 获取解析后的匿名类型
						anonymous_type = '高匿'
						# 获取解析后的协议类型
						protocol = td_content_list[4].get_text()
						# 拼接IP地址+端口号
						ipAndPort = ip+':'+port
						
						page_proxy_ip_detail_set.add((ipAndPort,anonymous_type,protocol))
					
			return page_proxy_ip_detail_set
			
		elif web_name == '66ip':
			# 解析获取的HTML数据
			for table_content in soup.find_all('table',{'width':'100%', 'border':'2px', 'cellspacing':'0px', 'bordercolor':'#6699ff'}):
				for tr_content in table_content.find_all('tr')[1:]:
					td_content_list = tr_content.find_all('td')
					
					
					# 获取解析后的IP地址
					ip = td_content_list[0].get_text()
					# 获取解析后的端口号
					port = td_content_list[1].get_text()
					# 获取解析后的匿名类型
					anonymous_type = '高匿'
					# 获取解析后的协议类型
					protocol = 'HTTP,HTTPS'
					# 拼接IP地址+端口号
					ipAndPort = ip+':'+port
					
					page_proxy_ip_detail_set.add((ipAndPort,anonymous_type,protocol))
					
			return page_proxy_ip_detail_set

		elif web_name == 'jiangxianli':
			# 解析获取的HTML数据
			for head_content in soup.find_all('head'):
				# 正则表达式，link标签中，href后以//数字开始
				for link_content in head_content.find_all(name='link', attrs={"href":re.compile('//\d')}):
					# 获取IP地址+端口号
					ipAndPort = link_content.get('href')[2:]
					# 获取解析后的匿名类型
					anonymous_type = '高匿'
					# 获取解析后的协议类型
					protocol = 'HTTP,HTTPS'

					page_proxy_ip_detail_set.add((ipAndPort, anonymous_type, protocol))

			return page_proxy_ip_detail_set



		else:
			print( 'There is no method to deal with \"{}\" website content, or check the \"collect_proxy_Ip.py\" to make sure there is a method to handle \"{}\"  website'.format(web_name, url))



if __name__ == "__main__":
	go = ParseIPWebContent()
	page_proxy_ip_detail_set = go.parse_web_content('https://ip.jiangxianli.com/?page=3&anonymity=2')
	print(page_proxy_ip_detail_set)