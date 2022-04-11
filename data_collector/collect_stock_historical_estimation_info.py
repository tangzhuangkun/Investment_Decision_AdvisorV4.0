import datetime
from datetime import date

import requests
import json
import time
import os
import sys

sys.path.append("..")
import database.db_operator as db_operator
import log.custom_logger as custom_logger
import main.get_conf_info as get_conf_info




class CollectStockHistoricalEstimationInfo:
    # 收集所需的股票的估值信息
    # PE-TTM :pe_ttm
    # PE-TTM(扣非) :d_pe_ttm
    # PB :pb
    # PS-TTM :ps_ttm
    # PCF-TTM :pcf_ttm
    # EV/EBIT :ev_ebit_r
    # 股票收益率 :ey
    # 股息率 :dyr
    # 股价 :sp
    # 成交量 :tv
    # 前复权 :fc_rights
    # 后复权 :bc_rights
    # 理杏仁前复权 :lxr_fc_rights
    # 股东人数 :shn
    # 市值 :mc
    # 流通市值 :cmc
    # 自由流通市值 :ecmc
    # 人均自由流通市值 :ecmc_psh
    # 融资余额 :fb
    # 融券余额 :sb
    # 陆股通持仓金额 :ha_shm

    # 运行频率：每天收盘后


    def __init__(self):
        # 从数据库取数时，每页取的条数信息
        # 每次向杏理仁请求数据时，每次申请的条数
        self.page_size = 80

        # 获取当前日期
        self.today = time.strftime("%Y-%m-%d", time.localtime())

    def get_all_exchange_locaiton_mics(self):
        '''
        获取所有交易所的mic码
        :return: mic码的list，如 ['XSHE', 'XHKG', 'XSHG']
        '''
        selecting_sql = "SELECT DISTINCT exchange_location_mic FROM all_tracking_stocks_rf"
        all_exchange_locaiton_mics_dict = db_operator.DBOperator().select_all("target_pool", selecting_sql)
        exchange_location_mic_list = list()
        for mic in all_exchange_locaiton_mics_dict:
            exchange_location_mic_list.append(mic.get("exchange_location_mic"))
        return exchange_location_mic_list

    def all_tracking_stocks(self, exchange_location_mic):
        '''
        数据库中，某交易所，全部需要被收集估值信息的股票
        :param exchange_location_mic: 交易所MIC码（如 XSHG, XSHE，XHKG）均可， 大小写均可
        :return:
        '''
        # 数据库中，全部需要被收集估值信息的股票
        # 输出： 需要被收集估值信息的股票代码，股票名称，上市地代码的字典
        # 如 [{'stock_code': '002688', 'stock_name': '金河生物', 'exchange_location': 'sz', 'exchange_location_mic': 'XSHE'},
        #     {'stock_code': '603696', 'stock_name': '安记食品', 'exchange_location': 'sh', 'exchange_location_mic': 'XSHG'},
        #     {'stock_code': '002234', 'stock_name': '民和股份', 'exchange_location': 'sz', 'exchange_location_mic': 'XSHE'},
        #     {'stock_code': '00700', 'stock_name': '腾讯控股', 'exchange_location': 'hk', 'exchange_location_mic': 'XHKG'},,, , , ]

        # 统一处理为大写
        exchange_location_mic = exchange_location_mic.upper()

        selecting_sql = """SELECT DISTINCT stock_code, stock_name, exchange_location, exchange_location_mic 
                            FROM all_tracking_stocks_rf where exchange_location_mic = '%s' """ % (exchange_location_mic)
        all_tracking_stock_dict = db_operator.DBOperator().select_all("target_pool", selecting_sql)
        # stock_codes_names_dict 如  [{'stock_code': '002688', 'stock_name': '金河生物', 'exchange_location': 'sz', 'exchange_location_mic': 'XSHE'},
        # {'stock_code': '603696', 'stock_name': '安记食品', 'exchange_location': 'sh', 'exchange_location_mic': 'XSHG'},
        # {'stock_code': '002234', 'stock_name': '民和股份', 'exchange_location': 'sz', 'exchange_location_mic': 'XSHE'},
        # {'stock_code': '00700', 'stock_name': '腾讯控股', 'exchange_location': 'hk', 'exchange_location_mic': 'XHKG'},,, , , ]
        return all_tracking_stock_dict

    def all_tracking_stocks_counter(self,exchange_location_mic):
        '''
        数据库中，某交易所，全部需要被收集估值信息的股票的统计数
         :param exchange_location_mic: 交易所MIC码（如 XSHG, XSHE，XHKG）均可， 大小写均可
        :return: 统计数，如 108
        '''
        # 统一处理为大写
        exchange_location_mic = exchange_location_mic.upper()

        selecting_sql = """SELECT count(DISTINCT stock_code) as counter FROM all_tracking_stocks_rf 
                            where exchange_location_mic = '%s' """ % (exchange_location_mic)
        stock_codes_counter = db_operator.DBOperator().select_one("target_pool", selecting_sql)
        return stock_codes_counter['counter']

    def paged_demanded_stocks(self, exchange_location_mic, page, size):
        '''
        根据分页信息获取,某个交易所，哪些股票需要被收集估值信息
        :param exchange_location_mic: 交易所MIC码（如 XSHG, XSHE，XHKG）均可， 大小写均可
        :param page: 分页的页码
        :param size: 每页条数
        :return: 返回该页的 股票代码，股票名称，上市地代码 字典
        # 如：{{'000001': {'stock_code': '000001', 'stock_name': '平安银行', 'exchange_location': 'sz', 'exchange_location_mic': 'XSHE'},
        # '000002': {'stock_code': '000002', 'stock_name': '万科A', 'exchange_location': 'sz', 'exchange_location_mic': 'XSHE'},
        # '000031': {'stock_code': '000031', 'stock_name': '大悦城', 'exchange_location': 'sz', 'exchange_location_mic': 'XSHE'},
        # ,,,,}
        '''

        # 统一处理为大写
        exchange_location_mic = exchange_location_mic.upper()

        start_row = page*size
        selecting_sql = """SELECT DISTINCT stock_code, stock_name, exchange_location, exchange_location_mic 
                            FROM all_tracking_stocks_rf where exchange_location_mic = '%s' 
                            order by stock_code limit %d,%d """ % (exchange_location_mic,start_row,size)
        paged_stock_info = db_operator.DBOperator().select_all("target_pool", selecting_sql)
        paged_stock_code_info_dict = dict()
        for piece in paged_stock_info:
            paged_stock_code_info_dict[piece["stock_code"]] = piece
        return paged_stock_code_info_dict

    def page_counter_by_page_size_per_page(self,exchange_location_mic):
        '''
        按X个为一页，将总的股票个数分成多页
        :param exchange_location_mic: 交易所MIC码（如 XSHG, XSHE，XHKG）均可， 大小写均可
        :return: 需要被分成多少页, 如：3
        '''

        # 统一处理为大写
        exchange_location_mic = exchange_location_mic.upper()
        stock_codes_total_counter = self.all_tracking_stocks_counter(exchange_location_mic)

        # 如果分页后，有余数（即未满一页的）
        if stock_codes_total_counter%self.page_size > 0:
            # 总页数需要加1
            page_counter = (stock_codes_total_counter//self.page_size) +1
        # 如果分页后，刚好分完，无余数
        else:
            page_counter = stock_codes_total_counter // self.page_size
        return page_counter

    def get_lxr_token(self):
        # 随机获取一个理杏仁的token、
        # 输出：理杏仁的token
        return get_conf_info.GetConfInfo().get_lxr_token()

    def tell_exchange_market_and_determine_url(self, exchange_location_mic):
        '''
        # 判断股票属于哪个交易市场，并决定使用哪个基本面数据URL
        :param exchange_location_mic: 交易所MIC码（如 XSHG, XSHE，XHKG）均可， 大小写均可
        :return: 使用理杏仁哪个URL来获取数据
        '''

        # 上市地代码或mic码，转为大写
        exchange_location_mic = exchange_location_mic.upper()

        # 如果为 上海，上交所，深圳，深交所
        if(exchange_location_mic=='XSHG' or exchange_location_mic=='XSHE'):
            return 'https://open.lixinger.com/api/cn/company/fundamental/non_financial'
        # 如果为 香港，港交所
        elif (exchange_location_mic=='XHKG'):
            return 'https://open.lixinger.com/api/hk/company/fundamental/non_financial'
        else:
            # 日志记录失败
            msg = exchange_location_mic + ' 该交易所MIC码不可用'
            custom_logger.CustomLogger().log_writter(msg, 'error')
            return 'Unavailable Market Code'

    def tell_exchange_market_and_determine_what_estimations_need_to_get(self, exchange_location_mic):
        '''
        # 判断股票属于哪个交易市场，并决定需要获取哪些指标
        :param exchange_location_mic: 交易所MIC码（如 XSHG, XSHE，XHKG）均可， 大小写均可
        :return:
        # 接口参数，PE-TTM :pe_ttm
        # PE-TTM(扣非) :d_pe_ttm
        # PB :pb
        # PS-TTM :ps_ttm
        # PCF-TTM :pcf_ttm
        # EV/EBIT :ev_ebit_r
        # 股票收益率 :ey
        # 股息率 :dyr
        # 股价 :sp
        # 成交量 :tv
        # 前复权 :fc_rights
        # 后复权 :bc_rights
        # 理杏仁前复权 :lxr_fc_rights
        # 股东人数 :shn
        # 市值 :mc
        # 流通市值 :cmc
        # 自由流通市值 :ecmc
        # 人均自由流通市值 :ecmc_psh
        # 融资余额 :fb
        # 融券余额 :sb
        # 陆股通持仓金额 :ha_shm

        # 如果为 上海，上交所，深圳，深交所，
        ["pe_ttm", "d_pe_ttm", "pb", "pb_wo_gw", "ps_ttm", "pcf_ttm", "ev_ebit_r", "ey", "dyr", "sp", "tv",
        "fc_rights", "bc_rights", "lxr_fc_rights", "shn", "mc", "cmc", "ecmc", "ecmc_psh", "fb", "sb", "ha_shm"]

        # 如果为 香港，港交所
        ["pe_ttm", "pb", "ps_ttm", "pcf_ttm", "dyr", "sp", "tv", "fc_rights", "bc_rights", "lxr_fc_rights", "shn", "mc"]
        '''
        # 上市地代码或mic码，转为大写
        exchange_location_mic = exchange_location_mic.upper()
        # 如果为上交所，深交所
        if (exchange_location_mic == 'XSHG' or exchange_location_mic == 'XSHE'):
            return ["pe_ttm", "d_pe_ttm", "pb", "pb_wo_gw", "ps_ttm", "pcf_ttm", "ev_ebit_r", "ey", "dyr", "sp", "tv",
                     "fc_rights", "bc_rights", "lxr_fc_rights", "shn", "mc", "cmc", "ecmc", "ecmc_psh", "fb", "sb",
                     "ha_shm"]
        # 如果为 港交所
        elif (exchange_location_mic == 'XHKG'):
            return ["pe_ttm", "pb", "ps_ttm", "pcf_ttm", "dyr", "sp", "tv", "fc_rights", "bc_rights", "lxr_fc_rights", "mc"]
        else:
            # 日志记录失败
            msg = exchange_location_mic + ' 该上市地代码不可用'
            custom_logger.CustomLogger().log_writter(msg, 'error')
            return 'Unavailable Market Code'

    def collect_a_period_time_estimation(self, stock_code, stock_info_dict, start_date, end_date):
        # 调取理杏仁接口，获取单个股票一段时间范围内，该股票估值数据, 并储存
        # param: stock_code, 股票代码, 如 000001
        # param:  stock_info_dict 股票代码,名称,上市地 字典, 只能1支股票，
        #         如  {'000001': {'stock_code': '000001', 'stock_name': '平安银行', 'exchange_location': 'sz', 'exchange_location_mic': 'XSHE'}}
        # param:  start_date, 开始时间，如 2020-11-12
        # param:  end_date, 结束时间，默认为空，如 2020-11-13
        # 输出： 将获取到股票估值数据存入数据库

        # 随机获取一个token
        token = self.get_lxr_token()
        # 理杏仁要求 在请求的headers里面设置Content-Type为application/json。
        headers = {'Content-Type': 'application/json'}
        # 判断股票属于哪个交易市场，并决定使用理杏仁哪个获取基本面数据URL
        # 理杏仁 获取基本面数据 接口
        url = self.tell_exchange_market_and_determine_url(stock_info_dict.get(stock_code).get('exchange_location'))
        # 判断股票属于哪个交易市场，并决定需要获取哪些指标
        estimations_list = self.tell_exchange_market_and_determine_what_estimations_need_to_get(stock_info_dict.get(stock_code).get('exchange_location'))

        parms = {"token": token,
                 "startDate": start_date,
                 "endDate": end_date,
                 "stockCodes":
                     [stock_code],
                 "metricsList": estimations_list}
        # 日志记录
        #msg = '向理杏仁请求的接口参数 ' + str(parms)
        #custom_logger.CustomLogger().log_writter(msg, 'info')
        values = json.dumps(parms)
        # 调用理杏仁接口
        req = requests.post(url, data=values, headers=headers)
        content = req.json()

        # 日志记录
        #msg = '理杏仁接口返回 ' + str(content)
        #custom_logger.CustomLogger().log_writter(msg, 'info')

        # content 如 {'code': 0, 'message': 'success', 'data': [{'date': '2020-11-13T00:00:00+08:00', 'pe_ttm': 48.04573277785343, 'd_pe_ttm': 47.83511443886097, 'pb': 14.42765025023379, 'pb_wo_gw': 14.42765025023379, 'ps_ttm': 22.564315310000808, 'pcf_ttm': 49.80250701327664, 'ev_ebit_r': 33.88432187818624, 'ey': 0.029323867066169462, 'dyr': 0.00998533724340176, 'sp': 1705, 'tv': 2815500, 'shn': 114300, 'mc': 2141817249000, 'cmc': 2141817249000, 'ecmc': 899670265725, 'ecmc_psh': 7871131, 'ha_shm': 173164289265, 'fb': 17366179363, 'sb': 2329851810, 'fc_rights': 1705, 'bc_rights': 1705, 'lxr_fc_rights': 1705, 'stockCode': '600519'}, {'date': '2020-11-12T00:00:00+08:00', 'pe_ttm': 48.88519458398379, 'd_pe_ttm': 48.67089629172529, 'pb': 14.679732186277464, 'pb_wo_gw': 14.679732186277464, 'ps_ttm': 22.95856220330575, 'pcf_ttm': 50.672663426136175, 'ev_ebit_r': 34.47543387050795, 'ey': 0.028824017925678805, 'dyr': 0.009813867960963575, 'sp': 1734.79, 'tv': 2347300, 'shn': 114300, 'mc': 2179239381462, 'cmc': 2179239381462, 'ecmc': 915389431248, 'ecmc_psh': 8008656, 'ha_shm': 176618263840, 'fb': 17207679699, 'sb': 2426239128, 'fc_rights': 1734.79, 'bc_rights': 1734.79, 'lxr_fc_rights': 1734.79, 'stockCode': '600519'}]}


        if 'error' in content and content.get('error').get('message') == "Illegal token.":
            # 日志记录失败
            msg = '使用无效TOKEN ' + token + ' ' + '执行函数collect_a_special_date_estimation时失败 ' + \
                  stock_code + ' ' +str(stock_info_dict.get(stock_code).get('stock_name')) + ' ' + start_date + ' ' + end_date
            custom_logger.CustomLogger().log_writter(msg, 'error')
            return self.collect_a_period_time_estimation(stock_code, stock_info_dict, start_date, end_date)

        try:
            # 数据存入数据库
            self.save_content_into_db(content, stock_info_dict, "period")
        except Exception as e:
            # 日志记录失败
            msg = '数据存入数据库失败。 ' + '理杏仁接口返回为 '+str(content) + '。 抛错为 '+ str(e) + ' 使用的Token为' + token
            custom_logger.CustomLogger().log_writter(msg, 'error')

    # TODO 此处之上的函数均已修正，此处以下的函数仍需修改及验证
    def collect_a_special_date_estimation(self, stock_info_dicts, date):
        # 调取理杏仁接口，获取特定一天，一只/多支股票估值数据, 并储存
        # param:  stock_info_dicts 股票代码,名称,上市地 字典, 1/多支股票，
        #         如  {{'000001': {'stock_code': '000001', 'stock_name': '平安银行', 'exchange_location': 'sz', 'exchange_location_mic': 'XSHE'},
        #         # '000002': {'stock_code': '000002', 'stock_name': '万科A', 'exchange_location': 'sz', 'exchange_location_mic': 'XSHE'},,,,}
        # param:  date, 日期，如 2020-11-12
        # 输出： 将获取到股票估值数据存入数据库


        # 随机获取一个token
        token = self.get_lxr_token()
        # 理杏仁要求 在请求的headers里面设置Content-Type为application/json。
        headers = {'Content-Type': 'application/json'}
        # 理杏仁 获取基本面数据 接口
        # url = 'https://open.lixinger.com/api/a/stock/fundamental/non_financial'
        url = 'https://open.lixinger.com/api/a/company/fundamental/non_financial'
        # 接口参数，
        # PE-TTM :pe_ttm
        # PE-TTM(扣非) :d_pe_ttm
        # PB :pb
        # PS-TTM :ps_ttm
        # PCF-TTM :pcf_ttm
        # EV/EBIT :ev_ebit_r
        # 股票收益率 :ey
        # 股息率 :dyr
        # 股价 :sp
        # 成交量 :tv
        # 前复权 :fc_rights
        # 后复权 :bc_rights
        # 理杏仁前复权 :lxr_fc_rights
        # 股东人数 :shn
        # 市值 :mc
        # 流通市值 :cmc
        # 自由流通市值 :ecmc
        # 人均自由流通市值 :ecmc_psh
        # 融资余额 :fb
        # 融券余额 :sb
        # 陆股通持仓金额 :ha_shm
        parms = {"token": token,
                 "date": date,
                 "stockCodes":
                     list(stock_info_dicts.keys()),
                 "metricsList": [
                     "pe_ttm", "d_pe_ttm", "pb", "pb_wo_gw", "ps_ttm", "pcf_ttm", "ev_ebit_r", "ey", "dyr", "sp", "tv",
                     "fc_rights", "bc_rights", "lxr_fc_rights", "shn", "mc", "cmc", "ecmc", "ecmc_psh", "fb", "sb",
                     "ha_shm"
                 ]}
        # 日志记录
        #msg = '向理杏仁请求的接口参数 ' + str(parms)
        #custom_logger.CustomLogger().log_writter(msg, 'info')

        values = json.dumps(parms)
        req = requests.post(url, data=values, headers=headers)
        content = req.json()
        # 日志记录
        #msg = '理杏仁接口返回 ' + str(content)
        #custom_logger.CustomLogger().log_writter(msg, 'info')

        # content 如 {'code': 0, 'message': 'success', 'data': [
        # {'date': '2020-11-13T00:00:00+08:00', 'pe_ttm': 48.2957825939533, 'd_pe_ttm': 48.62280236330014, 'pb': 12.491374104141297, 'pb_wo_gw': 12.491374104141297, 'ps_ttm': 17.156305422424143, 'pcf_ttm': 63.68585789882434, 'ev_ebit_r': 37.63760421342357, 'ey': 0.026088654822125818, 'dyr': 0.0085167925205312, 'sp': 186.69, 'tv': 13479800, 'shn': 113900, 'mc': 273454640491.19998, 'cmc': 273371391686, 'ecmc': 133902847844, 'ecmc_psh': 1175618, 'ha_shm': 5559655830, 'fc_rights': 186.69, 'bc_rights': 186.69, 'lxr_fc_rights': 186.69, 'stockCode': '000568'}, {'date': '2020-11-13T00:00:00+08:00', 'pe_ttm': 60.72940789130697, 'd_pe_ttm': 64.53258136924804, 'pb': 11.823197225442007, 'pb_wo_gw': 12.43465627328832, 'ps_ttm': 11.182674688897702, 'pcf_ttm': 216.59317739098543, 'ev_ebit_r': 48.032852603259784, 'ey': 0.02045252811485187, 'dyr': 0.006568863586599518, 'sp': 228.35, 'tv': 3310800, 'shn': 31900, 'mc': 114997060000, 'cmc': 87595060000, 'ecmc': 25619951576, 'ecmc_psh': 803133, 'ha_shm': 1181857851, 'fc_rights': 228.35, 'bc_rights': 228.35, 'lxr_fc_rights': 228.35, 'stockCode': '000596'}]}

        if 'message' in content and content['message'] == "Illegal token.":
            # 日志记录失败
            msg = 'Failed to use token ' + token + ' ' + 'to collect_a_special_date_estimation of ' + \
                  str(stock_codes_names_dict) + ' ' + date + ' 报错token为 ' + token
            custom_logger.CustomLogger().log_writter(msg, 'error')
            return self.collect_a_special_date_estimation(stock_codes_names_dict, date)

        try:
            # 数据存入数据库
            self.save_content_into_db(content, stock_codes_names_dict, "date")
        except Exception as e:
            # 日志记录失败
            msg = '数据存入数据库失败。 ' + '理杏仁接口返回为 ' + str(content) + '。 抛错为 ' + str(e) + ' 使用的token为 ' + token
            custom_logger.CustomLogger().log_writter(msg, 'error')


        '''
        message = content['message']
        # 检查token是否失效
        if message == "illegal token.":
            # 日志记录失败
            msg = 'Failed to use token ' + token + ' ' + 'to collect_a_period_time_estimation of ' + \
                  str(stock_codes_names_dict) + ' ' + date
            custom_logger.CustomLogger().log_writter(msg, 'error')
            return self.collect_a_period_time_estimation(stock_codes_names_dict, date)
        # 数据存入数据库
        self.save_content_into_db(content, stock_codes_names_dict, "date")
        '''


    def save_content_into_db(self, content, stock_codes_names_dict, range):
        # 将 理杏仁接口返回的数据 存入数据库
        # param:  content, 理杏仁接口返回的数据
        # param:  stock_codes_names_dict 股票代码名称字典, 可以1支/多支股票，
        # 如  {{'000001': {'stock_code': '000001', 'stock_name': '平安银行', 'exchange_location': 'sz', 'exchange_location_mic': 'XSHE'},
        #      '000002': {'stock_code': '000002', 'stock_name': '万科A', 'exchange_location': 'sz', 'exchange_location_mic': 'XSHE'}}
        # param： range， 时间范围，只能填 period 或者 date

        # 解析返回的数据
        for piece in content["data"]:
            stock_code = piece['stockCode']
            stock_name = stock_codes_names_dict.get(stock_code).get("stock_name")
            date = piece['date'][:10]
            # 上市地
            exchange_location = stock_codes_names_dict.get(stock_code).get("exchange_location")
            # 交易所mic码
            exchange_location_mic = stock_codes_names_dict.get(stock_code).get("exchange_location_mic")

            # 检查记录是否已在数据库中存在
            is_data_existing = self.is_existing(stock_code, stock_name, date)
            # 如果已存在，且获取的是，一只股在一段时间内的估值数据，则循环截止,不需要收集这一天和往前日期的数据
            if is_data_existing and range=="period":
                # 日志记录
                msg = stock_code + " "+ stock_name+ "在"+ date+" 之前的估值数据已经存在，无需再存此日期之前的数据。"
                custom_logger.CustomLogger().log_writter(msg, 'info')
                break
            # 如果已存在，且获取的是，一/多只股在特定日期的估值数据，则停止收集该只数据，切换至下一个
            elif is_data_existing and range=="date":
                # 日志记录
                msg = stock_code + " " + stock_name + date + "的估值数据已经存在，无需再存此日期的数据。"
                custom_logger.CustomLogger().log_writter(msg, 'info')
                continue

            # 如果获取不到值，则置为0，避免出现 keyerror
            pe_ttm = piece.setdefault('pe_ttm', 0)
            pe_ttm_nonrecurring = piece.setdefault('d_pe_ttm', 0)
            pb = piece.setdefault('pb', 0)
            pb_wo_gw = piece.setdefault('pb_wo_gw', 0)
            ps_ttm = piece.setdefault('ps_ttm', 0)
            pcf_ttm = piece.setdefault('pcf_ttm', 0)
            ev_ebit = piece.setdefault('ev_ebit_r', 0)
            stock_yield = piece.setdefault('ey', 0)
            dividend_yield = piece.setdefault('dyr', 0)
            share_price = piece.setdefault('sp', 0)
            turnover = piece.setdefault('tv', 0)
            fc_rights = piece.setdefault('fc_rights', 0)
            bc_rights = piece.setdefault('bc_rights', 0)
            lxr_fc_rights = piece.setdefault('lxr_fc_rights', 0)
            shareholders = piece.setdefault('shn', 0)
            market_capitalization = piece.setdefault('mc', 0)
            circulation_market_capitalization = piece.setdefault('cmc', 0)
            free_circulation_market_capitalization = piece.setdefault('ecmc', 0)
            free_circulation_market_capitalization_per_capita = piece.setdefault('ecmc_psh', 0)
            financing_balance = piece.setdefault('fb', 0)
            securities_balances = piece.setdefault('sb', 0)
            stock_connect_holding_amount = piece.setdefault('ha_shm', 0)

            # 存入数据库
            inserting_sql = "INSERT IGNORE INTO stocks_main_estimation_indexes_historical_data (stock_code, stock_name, date, exchange_location, exchange_location_mic, pe_ttm,pe_ttm_nonrecurring,pb,pb_wo_gw,ps_ttm,pcf_ttm,ev_ebit,stock_yield,dividend_yield,share_price,turnover,fc_rights,bc_rights,lxr_fc_rights,shareholders,market_capitalization,circulation_market_capitalization,free_circulation_market_capitalization,free_circulation_market_capitalization_per_capita,financing_balance,securities_balances,stock_connect_holding_amount ) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s' )" % (
            stock_code, stock_name, date, exchange_location, exchange_location_mic, pe_ttm, pe_ttm_nonrecurring, pb, pb_wo_gw, ps_ttm, pcf_ttm, ev_ebit,
            stock_yield, dividend_yield, share_price, turnover, fc_rights, bc_rights, lxr_fc_rights, shareholders,
            market_capitalization, circulation_market_capitalization, free_circulation_market_capitalization,
            free_circulation_market_capitalization_per_capita, financing_balance, securities_balances,
            stock_connect_holding_amount)
            db_operator.DBOperator().operate("insert", "financial_data", inserting_sql)

        # 日志记录
        #msg = str(stock_codes_names_dict) + '\'s estimation info has been saved '
        #custom_logger.CustomLogger().log_writter(msg, 'info')

    def is_existing(self, stock_code, stock_name, date):
        # 检查数据库中是否有记录，主要是检查是否为同一支股票同一日期
        # param: stock_code, 股票代码
        # param: stock_name，股票名称
        # param: date，日期
        # 输出：True，已存在； False，无记录

        selecting_sql = "SELECT pe_ttm FROM stocks_main_estimation_indexes_historical_data where stock_code = '%s' and stock_name = '%s' and date = '%s' " % (stock_code, stock_name, date)
        existing = db_operator.DBOperator().select_one("financial_data", selecting_sql)

        # 如果查询结果为None，则说明不存在；否则，说明有记录
        if existing == None:
            return False
        else:
            return True

    def collect_all_new_stocks_info_at_one_time(self, start_date, stock_codes_names_dict):
        # 将所有新的，且需要被收集估值信息的股票，一次性收集数据
        # param: start_date, 起始日期，如 2010-01-02
        # param: stock_codes_names_dict 股票代码名称字典, 可以1支/多支股票， 如  {"000568":"泸州老窖", "000596":"古井贡酒",,,}

        # 遍历股票
        for k, v in stock_codes_names_dict.items():
            piece_dict = {k: v}
            # 收集单只股票，如从2010-01-01至今的估值数据
            self.collect_a_period_time_estimation(piece_dict, start_date, self.today)

    def collect_all_new_stocks_info_at_one_time_in_batch(self,start_date):
        # 分批次，将所有新的，且需要被收集估值信息的股票，从起始日期开始，全部收集
        # param: start_date, 起始日期，如 2010-01-02

        # 总共需要将采集的股票数分成多少页，即分成多少批次
        page_counter = self.page_counter_by_page_size_per_page()
        # 日志记录
        msg = '共需收集 ' + str(page_counter) + ' 页的股票估值信息'
        custom_logger.CustomLogger().log_writter(msg, 'info')
        for page in range(page_counter):
            stock_codes_names_dict_in_page = self.paged_demanded_stocks(page, self.page_size)
            try:
                self.collect_all_new_stocks_info_at_one_time(start_date,stock_codes_names_dict_in_page)
                # 日志记录
                msg = '收集了第 ' + str(page + 1) + ' 页的股票估值信息'
                custom_logger.CustomLogger().log_writter(msg, 'info')
            except Exception as e:
                # 日志记录
                msg = '收集到第 ' + str(page + 1) + ' 页的股票估值信息时' + '发生错误 ' + str(e)
                custom_logger.CustomLogger().log_writter(msg, 'error')


    def collect_stocks_recent_info(self, stock_codes_names_dict, processing_date):
        # 收集当前所有股票特定日期的的信息
        # param: processing_date, 需要收集的日期
        # param: stock_codes_names_dict 股票代码名称字典, 可以1支/多支股票， 如  {"000568":"泸州老窖", "000596":"古井贡酒",,,}

        # 收集数据库中所有股票，今日的估值数据
        try:
            self.collect_a_special_date_estimation(stock_codes_names_dict, processing_date)
            # 日志记录
            msg = '收集了 '+ processing_date +'  '+ str(stock_codes_names_dict) +' 的股票估值信息'
            custom_logger.CustomLogger().log_writter(msg, 'info')
        except Exception as e:
            # 日志记录
            msg = '在收集 ' + processing_date +'  '+ str(stock_codes_names_dict) + ' 的股票估值信息时' + '发生错误 ' + str(e)
            custom_logger.CustomLogger().log_writter(msg, 'error')

    def collect_stocks_recent_info_in_batch(self, start_date):
        # param: start_date, 起始日期，如 2010-01-02
        # 分批次，收集当前所有股票最近的信息

        plus_one_day = datetime.timedelta(days=1)
        start_date = self.latest_collection_date(start_date)+plus_one_day
        today_date = date.today()
        while start_date <= today_date:
            # 总共需要将采集的股票数分成多少页，即分成多少批次
            page_counter = self.page_counter_by_page_size_per_page()
            # 日志记录
            #msg = '共需收集 ' + str(page_counter) + ' 页的股票估值信息'
            #custom_logger.CustomLogger().log_writter(msg, 'info')
            for page in range(page_counter):
                stock_codes_names_dict_in_page = self.paged_demanded_stocks(page,self.page_size)
                # 收集当前页内所有股票特定日期的的信息
                self.collect_stocks_recent_info(stock_codes_names_dict_in_page,str(start_date))
            start_date += plus_one_day

    def latest_collection_date(self,start_date):
        # 获取数据库中最新收集股票估值信息的日期
        # param: start_date, 起始日期，如 2010-01-02
        # 返回 如果数据库有最新的日期，则返回最新收集股票估值信息的日期，类型为datetime.date， 如 2021-05-14
        #     如果数据库无最新的日期，返回起始日期的前一天

        selecting_sql = "SELECT max(date) as date FROM stocks_main_estimation_indexes_historical_data"
        latest_collection_date = db_operator.DBOperator().select_one("financial_data", selecting_sql)
        # 如果数据库无最新的日期，为空
        if latest_collection_date['date'] == None:
            plus_one_day = datetime.timedelta(days=1)
            # 返回起始日期的前一天，后续才能从 起始日期开始处理
            return datetime.date(int(start_date[:4]),int(start_date[5:7]),int(start_date[8:10]))-plus_one_day
        return latest_collection_date['date']

    def test_date_loop(self):

        plus_one_day = datetime.timedelta(days=1)
        start_date = self.latest_collection_date()+plus_one_day
        today_date = date.today()

        while start_date<=today_date:
            print(str(start_date))
            start_date += plus_one_day



    def main(self,start_date):
        # 与上次数据库中待收集的股票代码和名称对比，
        # 并决定是 同时收集多只股票特定日期的数据 还是 分多次收集个股票一段时间的数据
        # param: start_date, 起始日期，如 2010-01-02

        # TODO， 获取所有交易所代码，按交易所逐个收集股票估值信息
        # 当前数据库中，待收集的股票代码和名称
        all_stock_codes_names_dict = self.all_tracking_stocks()

        # 获取文件的当前路径（绝对路径）
        cur_path = os.path.dirname(os.path.realpath(__file__))
        # 获取comparison.json的路径
        json_path = os.path.join(cur_path, 'comparison.json')
        with open(json_path, 'r', encoding='utf-8') as com:
            last_time_data = json.load(com)

        # 如果待收集的内容与上次数据库中的一致
        # 则只收集最近日期的
        if all_stock_codes_names_dict == last_time_data["last_time_stock_codes_names_in_db_dict"]:
            # 日志记录
            msg = '无新增的股票，开始收集最近交易日的股票估值信息 '
            custom_logger.CustomLogger().log_writter(msg, 'info')
            self.collect_stocks_recent_info_in_batch(start_date)
        # 如果不相同，则一次性收集所有数据
        else:
            # 日志记录
            msg = '有新增的股票，开始收集从 '+start_date+' 到 '+self.today +' 的股票估值信息 '
            custom_logger.CustomLogger().log_writter(msg, 'info')
            self.collect_all_new_stocks_info_at_one_time_in_batch(start_date)
            # 获取文件的当前路径（绝对路径）
            cur_path = os.path.dirname(os.path.realpath(__file__))
            # 获取comparison.json的路径
            json_path = os.path.join(cur_path, 'comparison.json')
            # 更新comparison文件中的记录
            with open(json_path, 'w', encoding='utf-8') as com:
                com.truncate()
                new_data = dict()
                new_data["last_time_stock_codes_names_in_db_dict"] = all_stock_codes_names_dict
                com.write(json.dumps(new_data, ensure_ascii=False))
            # 日志记录
            msg = '更新 comparison.json 的内容 '
            custom_logger.CustomLogger().log_writter(msg, 'info')

        # 日志记录
        msg = '已经收集了全部股票至今的历史估值信息'
        custom_logger.CustomLogger().log_writter(msg, 'info')


if __name__ == "__main__":
    time_start = time.time()
    go = CollectStockHistoricalEstimationInfo()
    #result = go.get_all_exchange_locaiton_mics()
    #result = go.get_lxr_token()
    #print(result)
    #result = go.all_tracking_stocks("XHKG")
    #print(stock_codes_names_dict)
    #go.collect_a_period_time_estimation("00700", {"00700":{"stock_code": "00700", "stock_name": "腾讯控股", "exchange_location": "hk", "exchange_location_mic": "XHKG"}}, "2022-04-01", "2022-04-11")
    #go.collect_a_special_date_estimation({"000568":"泸州老窖", "000596":"古井贡酒"}, "2020-11-09")
    # print(content)
    #go.collect_all_new_stocks_info_at_one_time()
    #result = go.is_existing("000568", "泸州老窖", "2020-11-19")
    #print(result)
    # go.main("2010-01-01")
    #print(go.all_tracking_stocks_counter("XHKG"))
    #go.latest_collection_date("2021-04-01")
    #go.test_date_loop()
    #result = go.paged_demanded_stocks("XSHE",0,80)
    #result = go.tell_exchange_market_and_determine_url("XHKG")
    #result = go.page_counter_by_page_size_per_page("XSHG")
    result = go.tell_exchange_market_and_determine_what_estimations_need_to_get("XHKG")
    print(result)
    time_end = time.time()
    print('Time Cost: ' + str(time_end - time_start))
