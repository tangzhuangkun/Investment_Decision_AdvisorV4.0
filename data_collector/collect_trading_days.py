import requests
import json
import time
import sys

sys.path.append("..")
import config.joinquant_account_info as joinquant_account_info
import log.custom_logger as custom_logger
import database.db_operator as db_operator

class CollectTradingDays:
    # 从聚宽接口收集交易日
    # 运行频率：每天收盘后

    def __init__(self):

        # 因下面代码，在存入交易日期时，会存在重复插入的问题，会产生Warning
        # 但warning在Python中是不会被try except捕获的，所以首先修改它，让try except可以捕获warning
        #warnings.filterwarnings('error')
        pass

    def collect_all_trading_days(self):
        # 从joinquant获取所有的交易日期

        url, body, token = joinquant_account_info.JoinquantAccountInfo().get_token()
        body = {
            "method": "get_all_trade_days",
            "token": token
        }
        try:
            # 获取聚宽返回的指数构成信息
            response = requests.post(url, data=json.dumps(body))
            return response.text
        except Exception as e:
            # 日志记录
            msg = '无法从joinquant获取所有的交易日期' + '  ' + str(e)
            custom_logger.CustomLogger().log_writter(msg, 'error')


    def is_saved_or_not(self,trading_day):
        # 检查一个交易日期是否已经存在
        # trading_day: 交易日期，如 2021-06-09

        try:
            # 查询sql
            selecting_sql = "SELECT * FROM trading_days WHERE trading_date = '%s'" %(trading_day)
            # 查询
            selecting_result = db_operator.DBOperator().select_one("financial_data", selecting_sql)
            return selecting_result

        except Exception as e:
            # 日志记录
            msg = "无法查询交易日期 " +trading_day+" 是否存在数据库" + '  ' + str(e)
            custom_logger.CustomLogger().log_writter(msg, 'error')
            return None



    def save_a_trading_day_into_db(self, trading_day):
        # 将一个交易日期存入数据库
        # trading_day: 交易日期，如 2021-06-09

        # 是否存入成功的标志
        flag = True

        # 检查是否曾经存过该日期
        existOrNot = self.is_saved_or_not(trading_day)
        # 如果没有该日期的记录，则存入
        if existOrNot is None:
            # 插入sql
            inserting_sql = "INSERT IGNORE INTO trading_days (trading_date, area, source) VALUES ('%s', '%s', '%s')" \
                            % (trading_day, "中国大陆", "聚宽")
            # 将数据存入数据库
            db_operator.DBOperator().operate("insert", "financial_data", inserting_sql)
            return flag
        # 如果该日期存在记录，则返回
        else:
            flag = False
            return flag

    def save_all_trading_days_into_db(self):
        # 将获取到的，截止至今日的交易日期存入数据可

        # 获取所有的交易日期
        all_trading_days_str = self.collect_all_trading_days()
        # 将聚宽传回的交易日期信息，由string转化为list，便于处理
        all_trading_days_list = all_trading_days_str.replace('\n', ',').split(',')


        # 获取当前日期
        today = time.strftime("%Y-%m-%d", time.localtime())
        # 倒序遍历，从近的日期向远的日期遍历
        for i in range(len(all_trading_days_list)-1,-1,-1):
            # 如果日期大于今天日期，则略过
            if(all_trading_days_list[i]>today):
                continue
            # 否则存入数据库
            else:
                isSavedSuccessfully = self.save_a_trading_day_into_db(all_trading_days_list[i])
                # 如果存入失败，说明该交易日期已存在数据库中，往前的日期也在存在，无需再重复插入
                if not isSavedSuccessfully:
                    break

if __name__ == '__main__':
    go = CollectTradingDays()
    #result = go.collect_all_trading_days()
    #print(result)
    go.save_all_trading_days_into_db()
    #existOrNot = go.is_saved_or_not("2021-06-04")
    #print(existOrNot)