import sys
sys.path.append('..')
import database.db_operator as db_operator
import log.custom_logger as custom_logger
import threading
import parsers.check_IP_availability as check_IP_availability


class CheckSavedIPAvailability:
	# 检查数据库中保存的所有IP的可用性
	# 不可用的删除掉
	# 运行频率：每天
	
	def __init__(self):
		pass
		
	def get_all_db_IPs(self,db_name):
		# 获取所有的存量IP
		# db_name: 需要查询数据库的名称， 来自 db_config.py 的 DATABASES
		# 输出：IP_dict_list，如[{'ip_address': '95.216.228.204:3128'},,,,]
		
		# sql query查询所有已存的ip地址		
		sql = "SELECT ip_address from IP_availability"
		# 从数据库取出
		IP_dict_list = db_operator.DBOperator().select_all(db_name,sql)
		
		return IP_dict_list
		
	def delete_unavailable_ip(self,db_name,ip):
		# 如果ip地址已经失活，从数据库中删除
		# db_name: 需要查询数据库的名称， 来自 db_config.py 的 DATABASE
		# ip: IP地址
		
		#删除该无效的ip地址		
		sql="DELETE from IP_availability where ip_address='%s'" % (ip)
		db_operator.DBOperator().operate('delete', db_name, sql)
		
		# 日志记录	
		msg = sql
		custom_logger.CustomLogger().log_writter(msg,'debug')
		
	
	def check_ip_availability_and_delete_unable_from_DB(self,db_name,IP_dict_list):
		# db_name: 需要查询数据库的名称， 来自 db_config.py 的 DATABASE
		# IP_dict_list, 输入的是一个list，里面装有dict，形式如：[{'ip_address': '1.24.185.60:9999'}, ,,,]
		# 检查查询到的所有ip的可用性，如果不可用，则从数据库中删除
			
		for ip_dict in IP_dict_list:
			#挨个检查IP活性, 舍去端口号
			is_available = check_IP_availability.CheckIPAvailability().check_single_ip_availability(ip_dict['ip_address'])
			if not is_available:
				self.delete_unavailable_ip(db_name, ip_dict['ip_address'])	
				
	def multiple_threading_checking_saved_ips(self,db_name):
		# 多线程检查数据库中ip的有效性
		
		# 数据库中输出的是一个list，里面装有dict，形式如：[{‘ip_address’:'61.145.48.100:9999'},,,,,]
		IP_dict_list = self.get_all_db_IPs('parser_component')
		
		# 数据库中查询到的ip平均分成多份，每份至多处理15个
		every_section_has_ip_num = 15
		
		divided_ips_list_into_sections = []
		# 将查询到的ip分成以每个子list存有最多10个ip的大list   [[10个ip],[10个ip]...]
		for i in range(0, len(IP_dict_list), every_section_has_ip_num):
			divided_ips_list_into_sections.append(IP_dict_list[i:i + every_section_has_ip_num])	
		
		# 启用多线程
		running_threads = []
		for section_index in range(len(divided_ips_list_into_sections)):
			# 创建新线程
			running_thread = threading.Thread(target=self.check_ip_availability_and_delete_unable_from_DB,args=(db_name,divided_ips_list_into_sections[section_index]))	
			running_threads.append(running_thread)	
		
		# 开启新线程
		for mem in running_threads:
			mem.start()
			
		# 等待所有线程完成
		for mem in running_threads:
			mem.join()
		
		# 日志记录	
		msg = "Checked all saved IPs in multiple threading way "
		custom_logger.CustomLogger().log_writter(msg,'info')
	
	
	def main(self):
		self.multiple_threading_checking_saved_ips('parser_component')
		# 日志记录
		msg = 'Just checked saved IPs availability'
		custom_logger.CustomLogger().log_writter(msg, 'info')


if __name__ == "__main__":
	go = CheckSavedIPAvailability()
	go.main()
		