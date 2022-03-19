import sys
sys.path.append('..')
import log.custom_logger as custom_logger
import ipaddress
import requests


class CheckIPAvailability:
	# 检查单个IP的活性
	
	def __init__(self):
		pass
		
		
	def check_single_ip_availability(self,ip):
		# 输入单个IP，检测IP格式及活性, 是否仍然有效
		# ip: 地址+端口号 例如 61.145.48.100:9999
		# 输出 是否
		
		#请求响应头
		headers =  {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
		
		try:  
			# 先检查ip格式是否正确，可检查IPv4 和 IPv6
			is_ip_formate_right = ipaddress.ip_address(ip.split(":")[0])
			
			# 再检测列表中IP活性
			try:
				proxy = {
					'http':ip
				}
				url1 = 'https://www.baidu.com/'
				#遍历时，利用访问百度，设定timeout=1,即在1秒内，未收到响应就断开连接
				res = requests.get(url=url1,proxies=proxy,headers=headers,timeout=1)
				return True
			except BaseException as e:
				# 日志记录	
				msg = ip + str(e)
				custom_logger.CustomLogger().log_writter(msg,lev='debug')
				return False
			
			return True
			
		except Exception as e:
			# 日志记录	
			msg = ip + str(e)
			custom_logger.CustomLogger().log_writter(msg,lev='debug')
			return False
	
	

if __name__ == "__main__":
	go = CheckIPAvailability()
	result = go.check_single_ip_availability('61.145.48.100:9999')
	print(result)