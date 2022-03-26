/* --------- user：investor1 ------ */
/* --------- db：target_pool ------ */
/*创建一个表，index_target，用于存储基金标的,对应策略*/
USE  target_pool;
CREATE TABLE IF NOT EXISTS `index_target`(
    `id` MEDIUMINT NOT NULL AUTO_INCREMENT,
	`index_code`  VARCHAR(12) COMMENT '跟踪指数代码，如 399997',
	`index_name`  VARCHAR(50) COMMENT '跟踪指数名称，如 中证白酒指数',
    `exchange_location_1`  VARCHAR(10) DEFAULT NULL COMMENT '指数上市地1，如 sh,sz',
    `exchange_location_2`  VARCHAR(10) DEFAULT NULL COMMENT '指数上市地2，如 XSHG, XSHE',
    `index_company`  VARCHAR(20) NOT NULL COMMENT '指数开发公司',
	`hold_or_not`  tinyint(1) DEFAULT 0 COMMENT '当前是否持有,1为持有，0不持有',
	`valuation_method` VARCHAR(100) DEFAULT NULL COMMENT '估值方法, pb,pe,ps',
	`buy_and_hold_strategy`  VARCHAR(100) DEFAULT NULL COMMENT '买入持有策略',
	`sell_out_strategy` VARCHAR(100) DEFAULT NULL COMMENT '卖出策略',
	`monitoring_frequency` VARCHAR(20) DEFAULT 'daily' COMMENT '监控频率，secondly, minutely, hourly, daily, weekly, monthly, seasonally, yearly, periodically',
	`holder` VARCHAR(100) DEFAULT 'zhuangkun' COMMENT '标的持有人',
	`status` VARCHAR(100) DEFAULT 'active' COMMENT '标的监控策略状态，active，suspend，inactive',
	`p_day` DATE NOT NULL COMMENT '提交的日期',
	`submission_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
	UNIQUE INDEX (index_code, valuation_method, monitoring_frequency, holder),
	PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT '跟踪指数及跟踪策略标的池';

insert into index_target (index_code, index_name, exchange_location_1, exchange_location_2, index_company, valuation_method, p_day )
values ('399997','中证白酒','sz','XSHE','中证','pe','2021-12-16');

insert into index_target (index_code, index_name, exchange_location_1, exchange_location_2, index_company, valuation_method, p_day )
values ('399396','国证食品饮料行业','sz','XSHE','国证','pe','2021-12-16');

insert into index_target (index_code, index_name, exchange_location_1, exchange_location_2, index_company, valuation_method, p_day )
values ('000932','中证800消费','sh','XSHG','中证','pe','2021-12-16');

insert into index_target (index_code, index_name, exchange_location_1, exchange_location_2, index_company, valuation_method, p_day )
values ('399965','中证800地产','sz','XSHE','中证','pb','2021-12-16');

insert into index_target (index_code, index_name, exchange_location_1, exchange_location_2, index_company, valuation_method, p_day )
values ('399986','中证银行','sz','XSHE','中证','pb','2021-12-16');

insert into index_target (index_code, index_name, exchange_location_1, exchange_location_2, index_company, valuation_method, p_day )
values ('000036','中证上证消费','sh','XSHG','中证','pe','2021-12-16');


/* --------- user：investor1 ------ */
/* --------- db：target_pool ------ */
/*创建一个表，stock_target，用于存储股票标的,对应策略*/
USE  target_pool;
CREATE TABLE IF NOT EXISTS `stock_target`(
    `id` MEDIUMINT NOT NULL AUTO_INCREMENT,
	`stock_code`  VARCHAR(12) COMMENT '跟踪指数代码，如 399997',
	`stock_name`  VARCHAR(50) COMMENT '跟踪指数名称，如 中证白酒指数',
    `exchange_location_1`  VARCHAR(10) DEFAULT NULL COMMENT '指数上市地1，如 sh,sz',
    `exchange_location_2`  VARCHAR(10) DEFAULT NULL COMMENT '指数上市地2，如 XSHG, XSHE',
	`hold_or_not`  tinyint(1) DEFAULT 0 COMMENT '当前是否持有,1为持有，0不持有',
	`valuation_method` VARCHAR(100) DEFAULT NULL COMMENT '估值方法, pb,pe,ps',
	`trigger_value`  DECIMAL(6,2) NOT NULL COMMENT '估值触发绝对值值，如 pb估值时，0.95',
	`trigger_percent`  DECIMAL(6,2) NOT NULL COMMENT '估值触发历史百分比，如 10，即10%位置',
	`buy_and_hold_strategy`  VARCHAR(100) DEFAULT NULL COMMENT '买入持有策略',
	`sell_out_strategy` VARCHAR(100) DEFAULT NULL COMMENT '卖出策略',
	`monitoring_frequency` VARCHAR(20) DEFAULT 'minutely' COMMENT '监控频率，secondly, minutely, hourly, daily, weekly, monthly, seasonally, yearly, periodically',
	`holder` VARCHAR(100) DEFAULT 'zhuangkun' COMMENT '标的持有人',
	`status` VARCHAR(100) DEFAULT 'active' COMMENT '标的监控策略状态，active，suspend，inactive',
	`p_day` DATE NOT NULL COMMENT '提交的日期',
	`submission_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
	UNIQUE INDEX (stock_code, valuation_method, monitoring_frequency, holder),
	PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT '跟踪股票及跟踪策略标的池';

insert into stock_target (stock_code, stock_name, exchange_location_1, exchange_location_2, valuation_method, trigger_value, trigger_percent, p_day )
values ('000002','万科A','sz','XSHE','pb',0.9,5,'2021-12-16');

insert into stock_target (stock_code, stock_name, exchange_location_1, exchange_location_2, valuation_method, trigger_value, trigger_percent, p_day )
values ('600048','保利发展','sh','XSHG','pb',0.89,20,'2021-12-16');