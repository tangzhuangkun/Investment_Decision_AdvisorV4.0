#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Tang Zhuangkun

'''
# TODO
股票监控策略，处于绝对低估位置的行业龙头
满足条件：
1、沪深300成分股
2、公认的行业龙头，https://xueqiu.com/8132581807/216258901
3、有记录的交易日数据超过1500天--2500天，即至少超过6.17年--10年的上市时间，仅看10年以内的指标（每年约243个交易日）
4、涨幅超过x%，就抛出进行轮动，坚守纪律性；这个指标需要回测来判断；
5、实时PB, 实时PE, 实时扣非PE（当时涨跌幅*昨日扣非PE）处于处于历史最低水平，即 拉通历史来看，处于倒数5位以内
'''


'''
-- 统计每年平均有多少个交易日
select avg(totoal_trading_days) from
(
select trading_year,count(*) as totoal_trading_days from
(select substr(trading_date,1,4) as trading_year
from trading_days
where trading_date<'2022-01-01'
) as raw
group by trading_year) raw_two

2005	242
2006	241
2007	242
2008	246
2009	244
2010	242
2011	244
2012	243
2013	238
2014	245
2015	244
2016	244
2017	244
2018	243
2019	244
2020	243
2021	243

'''



'''
-- 获取股票，股票名称，最新日期，市净率，市净率低估排名，共有该股票多少交易日记录，当前市净率位于历史百分比位置
select raw.stock_code, raw.stock_name, raw.date, raw.pb, raw.rank_num, record.total_record, raw.percent_num from
(select stock_code, stock_name, date, pb,
rank() OVER (partition by stock_code ORDER BY pb asc) AS rank_num,
percent_rank() OVER (partition by stock_code ORDER BY pb asc) AS percent_num
from stocks_main_estimation_indexes_historical_data) raw
left join
(select stock_code, count(*) as total_record from stocks_main_estimation_indexes_historical_data group by stock_code) as record
on raw.stock_code = record.stock_code
where raw.date = (select max(date) from stocks_main_estimation_indexes_historical_data)
order by raw.percent_num asc;

-- 效果如 
002946	新乳业	2022-04-07	3.8816476412805274	1	772	0
300741	华宝股份	2022-04-07	2.0352819414290860	1	995	0
300973	立高食品	2022-04-07	7.3017363381492615	1	235	0
600201	生物股份	2022-04-07	2.4402423138242970	1	2944	0
603317	天味食品	2022-04-07	3.1937266540248680	1	721	0
603517	绝味食品	2022-04-07	4.4156516446515500	2	1227	0.0008156606851549756
603866	桃李面包	2022-04-07	3.8300289940574705	3	1528	0.0013097576948264572
300783	三只松鼠	2022-04-07	4.5668188010520790	2	662	0.0015128593040847202
603983	丸美股份	2022-04-07	3.2240627734502910	2	653	0.0015337423312883436
600000	浦发银行	2022-04-07	0.4308040872445288	18	2929	0.005806010928961749
603719	良品铺子	2022-04-07	4.8572542850093390	4	513	0.005859375
601818	光大银行	2022-04-07	0.4847183905791494	18	2805	0.006062767475035664
600016	民生银行	2022-04-07	0.3489460092537104	23	2967	0.007417397167902899
603345	安井食品	2022-04-07	2.9889841653360740	11	1206	0.008298755186721992
300999	金龙鱼	2022-04-07	3.0021686825389193	4	358	0.008403361344537815
603043	广州酒家	2022-04-07	4.0568130239939570	13	1160	0.010353753235547885
601155	新城控股	2022-04-07	1.2309878673186585	18	1529	0.01112565445026178
601229	上海银行	2022-04-07	0.5305442247083050	18	1309	0.012996941896024464

'''






'''
-- 获取股票，股票名称，最新日期，扣非市盈率率，扣非市盈率率低估排名，共有该股票多少交易日记录，当前扣非市盈率率位于历史百分比位置

select raw.stock_code, raw.stock_name, raw.date, raw.pe_ttm_nonrecurring, raw.rank_num, record.total_record, raw.percent_num from
(select stock_code, stock_name, date, pe_ttm_nonrecurring,
rank() OVER (partition by stock_code ORDER BY pe_ttm_nonrecurring asc) AS rank_num,
percent_rank() OVER (partition by stock_code ORDER BY pe_ttm_nonrecurring asc) AS percent_num
from stocks_main_estimation_indexes_historical_data) raw
left join
(select stock_code, count(*) as total_record from stocks_main_estimation_indexes_historical_data group by stock_code) as record
on raw.stock_code = record.stock_code
where raw.date = (select max(date) from stocks_main_estimation_indexes_historical_data)
order by raw.percent_num asc;

-- 效果如 
300783	三只松鼠	2022-04-07	27.4111112081658880	1	662	0
300973	立高食品	2022-04-07	48.3345321582607900	1	235	0
002946	新乳业	2022-04-07	33.8728493011961900	2	772	0.0012970168612191958
603866	桃李面包	2022-04-07	26.4062387322165720	3	1528	0.0013097576948264572
603517	绝味食品	2022-04-07	22.8307804264350600	12	1227	0.00897226753670473
601229	上海银行	2022-04-07	4.2633774040877360	18	1309	0.012996941896024464
601528	瑞丰银行	2022-04-07	12.4534533226176390	4	188	0.016042780748663103
601997	贵阳银行	2022-04-07	3.9287532007183823	25	1368	0.01755669348939283
002511	中顺洁柔	2022-04-07	21.5256754399666370	52	2716	0.01878453038674033
605499	东鹏饮料	2022-04-07	47.9405319080057600	5	208	0.01932367149758454
600895	张江高科	2022-04-07	12.0794516852419630	60	2968	0.01988540613414223
601818	光大银行	2022-04-07	4.2020367359736280	60	2805	0.021041369472182596
603043	广州酒家	2022-04-07	23.1757056135805400	28	1160	0.023295944779982744
600928	西安银行	2022-04-07	6.5095449202036290	19	752	0.023968042609853527
600015	华夏银行	2022-04-07	3.7188474206319655	77	2957	0.02571041948579161
000876	新希望	2022-04-07	-14.8742832973529890	74	2788	0.026193039110154286
002958	青农商行	2022-04-07	6.6145207844781580	22	735	0.02861035422343324
601916	浙商银行	2022-04-07	5.7151968309404990	19	571	0.031578947368421054
'''

