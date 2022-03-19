import pymysql
import sys
sys.path.append('..')
import main.environment as environment
import config.db_config as db_config
import log.custom_logger as custom_logger

class DBOperator:
	# 数据库的基础操作，增删改查，
	# 使用数据库池以支持多线程操作
	
	def __init__(self):
		self.env = environment.Envirnment().tag_envirnment()
	
	def create_conn(self, db_name):
		# db_name：创建哪个模块的数据库连接池
		# 来自 db_config.py 的 DATABASES
		
		# 创建数据库连接池
		# 输出：与数据库的链接，数据库操作游标
		
		# 连接数据库
		conn = db_config.DATABASES[self.env][db_name].connection()
		# 数据库操作游标
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		return conn, cursor


	def close_conn(self, conn, cursor):
		# conn：数据库的链接
		# cursor：数据库操作游标
		
		# 关闭数据库链接和操作游标
		# 需按顺序，先关 操作游标，再关数据库链接
		cursor.close()
		conn.close()
	
	
	def select_one(self, db_name, sql):
		# db_name：创建哪个模块的数据库连接池
		# 来自 db_config.py 的 DATABASES
		# sql: 需要插入数据库的sql query
		# 查一个
		# 输出： 返回查询结果
		
		# 创建链接和操作游标
		conn, cur = self.create_conn(db_name)
		try:
			# 如果数据库连接失败，则重连
			conn.ping(reconnect=True)
			# 执行sql语句
			cur.execute(sql)
			# 获取结果
			result = cur.fetchone()
			# 关闭
			self.close_conn(conn, cur)
			# 返回查询结果
			return result
			
		except Exception as e:
			# 如果发生错误则回滚
			conn.rollback()
			print(e)
			# 关闭
			self.close_conn(conn, cur)
			


	def select_all(self, db_name,sql):
		# db_name：创建哪个模块的数据库连接池
		# 来自 db_config.py 的 DATABASES	
		# sql: 需要插入数据库的sql query
		# 查全部
		# 输出： 返回查询结果
		
		# 创建链接和操作游标
		conn, cur = self.create_conn(db_name)
		try:
			# 如果数据库连接失败，则重连
			conn.ping(reconnect=True)
			# 执行sql语句
			cur.execute(sql)
			# 获取结果
			result = cur.fetchall()
			# 关闭
			self.close_conn(conn, cur)
			# 返回查询结果
			return result
			
		except Exception as e:
			# 如果发生错误则回滚
			conn.rollback()
			# 关闭
			self.close_conn(conn, cur)
			# 日志记录
			msg = db_name+'  '+sql + '  '+ str(e)
			custom_logger.CustomLogger().log_writter(msg)
			
			
	def operate(self, action, db_name, sql):
		# action：必选，只能填 insert，delete，update
		# db_name：创建哪个模块的数据库连接池
		# 来自 db_config.py 的 DATABASES
		# sql: 需要删除数据库的sql query
		# 增，删，改
		
		# 检查action是否符合规范
		if action in ('insert','delete','update'):
		
			# 创建链接和操作游标
			conn, cur = self.create_conn(db_name)
			try:
				# 如果数据库连接失败，则重连
				conn.ping(reconnect=True)
				# 执行sql语句
				cur.execute(sql)
				# 提交
				conn.commit()
			except Exception as e:
				# 如果发生错误则回滚
				conn.rollback()

				# 忽略因为收集的IP与库中现存的IP重复出现的日志信息
				if db_name == 'parser_component' and e.args[0] == 1062:
					pass
				else:
					# 日志记录
					msg = db_name+'  '+sql + '  '+ str(e)
					custom_logger.CustomLogger().log_writter(msg)

			finally:
				# 关闭
				self.close_conn(conn, cur)
		else:
			# print("Wrong action,please reinput one")
			# 检查action不符合规范，只能填 insert，delete，update
			# 日志记录
			msg = "Wrong action,please reinput one, choose from (insert，delete，update)"
			custom_logger.CustomLogger().log_writter(msg)


if __name__ == "__main__":
	go = DBOperator()
	#conn, cursor = go.create_conn('parser_component')
	#print(conn)
	#print(cursor)
	# sql = ''
	#go.operate('insert','parser_component',sql)
