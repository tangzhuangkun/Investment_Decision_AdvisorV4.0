#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Tang Zhuangkun

class OperateTargetVo:
    '''
    对标的物进行操作，支持更新，创建
    所需用到的参数
    '''

    def __init__(self, target, operation, target_code, valuation_method, monitoring_frequency, holder, status,exchange_location):
        self._target = target
        self._operation = operation
        self._target_code = target_code
        self._valuation_method = valuation_method
        self._monitoring_frequency = monitoring_frequency
        self._holder = holder
        self._status = status
        self._exchange_location = exchange_location
    # 标的类型
    @property
    def target(self):
        return self._target
    @target.setter
    def target(self, target):
        self._target = target

    # 操作
    @property
    def operation(self):
        return self._operation
    @operation.setter
    def operation(self, operation):
        self._operation = operation

    # 标的代码
    @property
    def target_code(self):
        return self._target_code
    @target_code.setter
    def target_code(self, target_code):
        self._target_code = target_code

    # 估值策略
    @property
    def valuation_method(self):
        return self._valuation_method
    @valuation_method.setter
    def valuation_method(self, valuation_method):
        self._valuation_method = valuation_method

    # 监控频率
    @property
    def monitoring_frequency(self):
        return self._monitoring_frequency
    @monitoring_frequency.setter
    def monitoring_frequency(self, monitoring_frequency):
        self._monitoring_frequency = monitoring_frequency

    # 标的持有人
    @property
    def holder(self):
        return self._holder
    @holder.setter
    def holder(self, holder):
        self._holder = holder

    # 标的策略状态
    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, status):
        self._status = status

    # 标的上市地, 如 sz, sh, hk
    @property
    def exchange_location(self):
        return self.exchange_location
    @exchange_location.setter
    def exchange_location(self, exchange_location):
        self._exchange_location = exchange_location