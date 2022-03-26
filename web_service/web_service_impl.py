#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Tang Zhuangkun


class WebServericeImpl:

    def __init__(self):
        pass

    def operate_target_impl(self,operation_target_params):
        '''
        实现对标的物进行操作，支持更新，创建
        :param operation_target_params.operation: 操作，如 create, update, 必选
        :param operation_target_params.target: 标的类型，如 index, stock，必选
        :param operation_target_params.target_code: 标的代码，如 指数代码 399997，股票代码 600519，必选
        :param operation_target_params.exchange_location: 标的上市地, 如 sz, sh, hk， 创建时-必选，更新时-可选
        :param operation_target_params.valuation_method: 估值策略, 如 pb,pe,ps， 创建时-必选，更新时-可选
        :param operation_target_params.monitoring_frequency: 监控频率, secondly, minutely, hourly, daily, weekly, monthly, seasonally, yearly, periodically， 创建时-必选，更新时-可选
        :param operation_target_params.holder: 标的持有人，创建时，默认 zhuangkun-可选，更新时-可选
        :param operation_target_params.status: 标的策略状态，如 active，suspend，inactive  创建时，默认active-可选，更新时-可选
        :return:
        '''


