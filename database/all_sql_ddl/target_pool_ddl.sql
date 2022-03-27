/* --------- user：investor1 ------ */
/* --------- db：target_pool ------ */
/*创建一个表，investment_target，用于存储跟踪标的及策略池*/
USE  target_pool;
CREATE TABLE IF NOT EXISTS `investment_target`(
    `id` MEDIUMINT NOT NULL AUTO_INCREMENT,
    `target_type`  VARCHAR(30) NOT NULL COMMENT '跟踪标的类型，如 指数-index，股票-stock',
	`target_code`  VARCHAR(30)  NOT NULL COMMENT '跟踪标的代码，如 399997',
	`target_name`  VARCHAR(50) COMMENT '跟踪标的名称，如 中证白酒指数',
	`index_company`  VARCHAR(20) DEFAULT NULL COMMENT '指数开发公司',
    `exchange_location`  VARCHAR(10) NOT NULL COMMENT '标的上市地1，如 sh,sz',
    `exchange_location_mic`  VARCHAR(10) NOT NULL COMMENT '标的上市地MIC，如 XSHG, XSHE 等',
	`hold_or_not`  tinyint(1) DEFAULT 0 COMMENT '当前是否持有,1为持有，0不持有',
	`valuation_method` VARCHAR(20) NOT NULL COMMENT '估值方法, pb,pe,ps,dr,roe,peg 等',
	`trigger_value`  DECIMAL(6,2) NOT NULL COMMENT '估值触发绝对值值临界点，含等于，看指标具体该大于等于还是小于等于，如 pb估值时，0.95',
	`trigger_percent`  DECIMAL(6,2) NOT NULL COMMENT '估值触发历史百分比临界点，含等于，看指标具体该大于等于还是小于等于，如 10，即10%位置',
	`buy_and_hold_strategy`  VARCHAR(100) DEFAULT NULL COMMENT '买入持有策略',
	`sell_out_strategy` VARCHAR(100) DEFAULT NULL COMMENT '卖出策略',
	`monitoring_frequency` VARCHAR(20) DEFAULT 'minutely' COMMENT '监控频率，secondly, minutely, hourly, daily, weekly, monthly, seasonally, yearly, periodically',
	`holder` VARCHAR(100) DEFAULT 'zhuangkun' COMMENT '标的持有人',
	`status` VARCHAR(100) DEFAULT 'active' COMMENT '标的监控策略状态，active，suspend，inactive',
	`p_day` DATE NOT NULL COMMENT '提交的日期',
	`submission_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
	UNIQUE INDEX (target_type, target_code, exchange_location_mic, valuation_method, monitoring_frequency, holder),
	PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT '跟踪标的及策略池';


insert into investment_target (target_type, target_code, target_name, index_company, exchange_location,
                               exchange_location_mic, valuation_method, trigger_value, trigger_percent, monitoring_frequency, p_day)
values ('index', '399997','中证白酒','中证','sz','XSHE','pe', '25', '30', 'daily','2022-03-27');

insert into investment_target (target_type, target_code, target_name, index_company, exchange_location,
                               exchange_location_mic, valuation_method, trigger_value, trigger_percent, monitoring_frequency, p_day)
values ('index', '399396','国证食品饮料行业','国证','sz','XSHE','pe', '25', '30', 'daily','2022-03-27');

insert into investment_target (target_type, target_code, target_name, index_company, exchange_location,
                               exchange_location_mic, valuation_method, trigger_value, trigger_percent, monitoring_frequency, p_day)
values ('index', '000932','中证800消费','中证','sz','XSHE','pe', '25', '30', 'daily','2022-03-27');

insert into investment_target (target_type, target_code, target_name, index_company, exchange_location,
                               exchange_location_mic, valuation_method, trigger_value, trigger_percent, monitoring_frequency, p_day)
values ('index', '399965','中证800地产','中证','sz','XSHE','pb', '0.9', '2', 'daily','2022-03-27');

insert into investment_target (target_type, target_code, target_name, index_company, exchange_location,
                               exchange_location_mic, valuation_method, trigger_value, trigger_percent, monitoring_frequency, p_day)
values ('index', '399986','中证银行','中证','sz','XSHE','pb', '0.9', '2', 'daily','2022-03-27');

insert into investment_target (target_type, target_code, target_name, index_company, exchange_location,
                               exchange_location_mic, valuation_method, trigger_value, trigger_percent, monitoring_frequency, p_day)
values ('index', '000036','中证上证消费','中证','sz','XSHE','pe', '25', '30', 'daily','2022-03-27');



insert into investment_target (target_type, target_code, target_name, exchange_location,
                               exchange_location_mic, valuation_method, trigger_value, trigger_percent, monitoring_frequency, p_day)
values ('stock','000002','万科A','sz','XSHE','pb',0.9,5,'minutely','2022-03-27');

insert into investment_target (target_type, target_code, target_name, exchange_location,
                               exchange_location_mic, valuation_method, trigger_value, trigger_percent, monitoring_frequency, p_day)
values ('stock','600048','保利发展','sh','XSHG','pb',0.89,20,'minutely','2022-03-27');