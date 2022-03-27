#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Tang Zhuangkun

import sys
sys.path.append("..")
import log.custom_logger as custom_logger
import database.db_operator as db_operator

class WebServericeImpl:

    def __init__(self):
        pass


    def __check_exchange_location_param(self, exchange_location):
        '''
        检查上市地参数
        :param exchange_location: 标的上市地, 如 sz, sh, hk， 必选
        :return: 正确的话，返回交易所的MIC码；错误的话，返回None
        '''
        # 深圳证券交易所
        if (exchange_location == "sz"):
            exchange_location_mic = "XSHE"
        # 上海证券交易所
        elif (exchange_location == "sh"):
            exchange_location_mic = "XSHG"
        # 香港证券交易所
        elif (exchange_location == "hk"):
            exchange_location_mic = "XHKG"
        else:
            return None
        return exchange_location_mic

        """
            # 暂不支持美股监控
            # 纽约证券交易所
            elif(operation_target_params.exchange_location == "ny"):
                exchange_location_mic = "XNYS"
            # 纳斯达克
            elif (operation_target_params.exchange_location == "ny"):
                exchange_location_mic = "XNAS"
            # 美国证券交易所
            elif (operation_target_params.exchange_location == "ny"):
                exchange_location_mic = "XASE"
        """


    def __check_valuation_method(self,valuation_method):
        '''
        检查估值策略是否正确,
        :param valuation_method:
        :return: boolean，True或者False
        '''
        # 是否为 市净率，市盈率，市销率，股息率，净资产回报率，peg策略
        if(valuation_method in ["pb","pe","ps","dr","roe","peg"]):
            return True
        else:
            return False

    def __check_monitoring_frequency(self,monitoring_frequency):
        '''
        检查监控频率是否正确
        :param monitoring_frequency:
        :return: boolean，True或者False
        '''
        # 是否为 秒级，分级，时级，日级，周级，月级，季级，年级，周期级
        if (monitoring_frequency in ["secondly", "minutely", "hourly", "daily", "weekly", "monthly", "seasonally", "yearly", "periodically"]):
            return True
        else:
            return False

    # todo
    def _is_a_num(self,num_str):
        '''
        检查一个数是否为数字，包含整数，小数
        :param num_str:输入一个为str
        :return:
        '''
        # 清除前后空格
        num = num_str.strip()
        print(type(eval(num)))
        if (type(eval(num))=="float" or type(eval(num))=="int"):
            return True
        else:
            return False

    def operate_target_impl(self,operation_target_params):
        '''
        实现对标的物进行操作，支持更新，创建
        :param operation_target_params.operation: 操作，如 create, update, 必选
        :param operation_target_params.target_type: 标的类型，如 index, stock，必选
        :param operation_target_params.target_code: 标的代码，如 指数代码 399997，股票代码 600519，必选
        :param operation_target_params.target_name: 跟踪标的名称，如 中证白酒指数, 万科， 创建时-必选，更新时-可选
        :param operation_target_params.exchange_location: 标的上市地, 如 sz, sh, hk， 创建时-必选，更新时-可选
        :param operation_target_params.valuation_method: 估值策略, 如 pb,pe,ps， 创建时-必选，更新时-可选
        :param operation_target_params.trigger_value: 估值触发绝对值值临界点，含等于，看指标具体该大于等于还是小于等于，如 pb估值时，0.95, 创建时-必选，更新时-可选
        :param operation_target_params.trigger_percent: 估值触发历史百分比临界点，含等于，看指标具体该大于等于还是小于等于，如 10，即10%位置 创建时-必选，更新时-可选
        :param operation_target_params.monitoring_frequency: 监控频率, secondly, minutely, hourly, daily, weekly, monthly, seasonally, yearly, periodically， 创建时-必选，更新时-可选
        :param operation_target_params.index_company: 指数开发公司, 如中证，国证， 创建指数标的时-必选，更新指数标的时-可选
        :param operation_target_params.buy_and_hold_strategy: 买入持有策略, 创建时-可选，更新时-可选
        :param operation_target_params.sell_out_strategy: 卖出策略, 创建时-可选，更新时-可选
        :param operation_target_params.holder: 标的持有人，创建时，默认 zhuangkun-可选，更新时-可选
        :param operation_target_params.status: 标的策略状态，如 active，suspend，inactive  创建时，默认active-可选，更新时-可选
        :param operation_target_params.hold_or_not：当前是否持有,1为持有，0不持有  创建时，默认0-可选，更新时-可选
        :return:
        '''

        # 检查必选参数是否有传入
        if(operation_target_params.operation!="create" and operation_target_params.operation!="update" or operation_target_params.operation==None):
            return {"msg": "操作参数operation出错", "code":400, "status":"Failure"}

        if (operation_target_params.target_type != "index" and operation_target_params.target_type != "stock" or operation_target_params.target_type == None):
            return {"msg": "标的类型参数target_type出错", "code":400, "status":"Failure"}

        if (operation_target_params.target_code == None):
            return {"msg": "标的代码参数target_code出错", "code":400, "status":"Failure"}


        # 如果是创建新标的
        if(operation_target_params.operation=="create"):

            # 跟踪标的名称是否为空
            if (operation_target_params.target_name == None):
                return {"msg": "标的名称参数target_name为空", "code": 400, "status": "Failure"}

            # 检查上市地参数是否合乎规范
            exchange_location_mic = self.__check_exchange_location_param(operation_target_params.exchange_location)
            if(exchange_location_mic==None):
                return {"msg": "上市地参数exchange_location出错", "code":400, "status":"Failure"}

            # 检查估值策略是否正确
            is_valuation_method_right = self.__check_valuation_method(operation_target_params.valuation_method)
            if(not is_valuation_method_right):
                return {"msg": "估值策略参数valuation_method出错", "code":400, "status":"Failure"}

            # 估值触发绝对值值临界点是否为空
            if (operation_target_params.trigger_value == None):
                return {"msg": "估值触发绝对值值临界点参数trigger_value为空", "code": 400, "status": "Failure"}
            # 估值触发绝对值值临界点是否为数字
            if (not operation_target_params.trigger_value.isdigit()):
                print(operation_target_params.trigger_value)
                print(type(operation_target_params.trigger_value))
                print(not operation_target_params.trigger_value.isdigit())
                return {"msg": "估值触发绝对值值临界点参数trigger_value不是数值", "code": 400, "status": "Failure"}

            # 估值触发历史百分比临界点是否为空
            if (operation_target_params.trigger_percent == None):
                return {"msg": "指数开发公司参数trigger_percent为空", "code": 400, "status": "Failure"}
            # 估值触发历史百分比临界点是否为数字
            if (not operation_target_params.trigger_percent.isdigit()):
                return {"msg": "指数开发公司参数trigger_percent不是数值", "code": 400, "status": "Failure"}


            # 检查监控频率是否正确
            is_monitoring_frequency_right = self.__check_monitoring_frequency(operation_target_params.monitoring_frequency)
            if (not is_monitoring_frequency_right):
                return {"msg": "监控频率参数monitoring_frequency出错", "code":400, "status":"Failure"}



            if(operation_target_params.target_type == "index"):

                # 指数开发公司是否为空
                if (operation_target_params.index_company == None):
                    return {"msg": "指数开发公司参数index_company为空", "code":400, "status":"Failure"}

                # 插入的SQL
                inserting_sql = """INSERT INTO investment_target(target_type, target_code, target_name, 
                index_company, exchange_location, exchange_location_mic, hold_or_not, valuation_method, trigger_value, 
                trigger_percent, buy_and_hold_strategy, sell_out_strategy, monitoring_frequency, holder, status) 
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" \
                                % (operation_target_params.target_type, operation_target_params.target_code,
                                   operation_target_params.target_name, operation_target_params.index_company,
                                   operation_target_params.exchange_location, exchange_location_mic,operation_target_params.hold_or_not,
                                   operation_target_params.valuation_method, operation_target_params.trigger_value,
                operation_target_params.trigger_percent, operation_target_params.buy_and_hold_strategy ,
                                   operation_target_params.sell_out_strategy, operation_target_params.monitoring_frequency,
                                   operation_target_params.holder,operation_target_params.status)


                is_inserted_successfully_dict = db_operator.DBOperator().operate("insert", "target_pool", inserting_sql)
                if(is_inserted_successfully_dict.get("status")):
                    # 日志记录
                    msg = '创建新的指数标的-'+operation_target_params.target_name+'成功 '
                    return {"msg": msg, "code":200, "status":"Success"}
                else:
                    # 日志记录
                    msg = '创建新的指数标的失败 ' + is_inserted_successfully_dict.get("msg")
                    custom_logger.CustomLogger().log_writter(msg, 'error')
                    return {"msg": msg, "code":400, "status":"Failure"}

            elif(operation_target_params.target_type == "stock"):
                try:
                    # 插入的SQL
                    inserting_sql = """INSERT INTO investment_target(target_type, target_code, target_name, 
                    exchange_location, exchange_location_mic, hold_or_not, valuation_method, trigger_value, 
                    trigger_percent, buy_and_hold_strategy, sell_out_strategy, monitoring_frequency, holder, status) 
                                        VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" \
                                    % (operation_target_params.target_type, operation_target_params.target_code,
                                       operation_target_params.target_name,
                                       operation_target_params.exchange_location, exchange_location_mic,
                                       operation_target_params.hold_or_not,
                                       operation_target_params.valuation_method, operation_target_params.trigger_value,
                                       operation_target_params.trigger_percent,
                                       operation_target_params.buy_and_hold_strategy,
                                       operation_target_params.sell_out_strategy,
                                       operation_target_params.monitoring_frequency,
                                       operation_target_params.holder, operation_target_params.status)
                    db_operator.DBOperator().operate("insert", "target_pool", inserting_sql)
                    # 日志记录
                    msg = '创建新的股票标的-' + operation_target_params.target_name + '成功 '
                    return {"msg": msg, "code": 200, "status": "Success"}

                except Exception as e:
                    # 日志记录
                    msg = '创建新的股票标的失败 ' + str(e)
                    custom_logger.CustomLogger().log_writter(msg, 'error')
                    return {"msg": msg, "code": 400, "status": "Failure"}

        # 如果是更新标的
        elif(operation_target_params.operation=="update"):
            if (operation_target_params.target_type == "index"):
                pass
            elif (operation_target_params.target_type == "stock"):
                pass

if __name__ == '__main__':
    go = WebServericeImpl()
    result = go._is_a_num("4.5")
    print(result)