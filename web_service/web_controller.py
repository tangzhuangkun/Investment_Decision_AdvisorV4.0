#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Tang Zhuangkun

# 通过接口，网络与该决策系统互动

import sys
sys.path.append('..')
import web_service.web_service_impl as web_service_impl
import vo.operate_target_vo as operate_target_vo
from flask import Flask, request  # 引入request对象
app = Flask(__name__)

@app.route("/operate_target", methods=["POST"])
def operate_target():
    '''
    对标的物进行操作，支持更新，创建
    :return:
    '''

    # 获取请求参数
    # 标的类型，如 index, stock
    target = request.args.get("target")
    # 操作，如 create, update
    operation = request.args.get("operation")
    # 标的代码，如 指数代码 399997，股票代码 600519
    target_code = request.args.get("code")
    # 标的上市地, 如 sz, sh, hk
    exchange_location = request.args.get("exchange_location")
    # 估值策略, 如 pb,pe,ps
    valuation_method = request.args.get("method")
    # 监控频率, secondly, minutely, hourly, daily, weekly, monthly, seasonally, yearly, periodically
    monitoring_frequency = request.args.get("frequency")
    # 标的持有人
    holder = request.args.get("holder")
    # 标的策略状态，如 active，suspend，inactive
    status = request.args.get("status")


    # 包装成一个对象
    params = operate_target_vo.OperateTargetVo(target, operation, target_code, valuation_method, monitoring_frequency,
                                               holder, status, exchange_location)
    # 实现 更新，创建
    web_service_impl.WebServericeImpl().operate_target_impl(params)

    return 'Hello World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)