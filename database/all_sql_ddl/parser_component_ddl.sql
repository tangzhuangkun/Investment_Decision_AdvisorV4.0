/* --------- user：investor1 ------ */
/* --------- db：parser_component ------ */
/*创建一个表，IP_availability，用于记录ip的可用性 */

/*
USE parser_component;
CREATE TABLE IF NOT EXISTS `IP_availability`(
	`ip_address` VARCHAR(21) NOT NULL COMMENT '主键，ip的地址+端口号，最长可达21位，作为主键可确保数据库中的ip地址不会重复',
	`is_anonymous` BOOLEAN NOT NULL COMMENT '是否为高匿名，是为1，否为0',
	`is_available` BOOLEAN NOT NULL COMMENT '是否仍然可用，是为1，否为0',
	`type` VARCHAR(21) COMMENT 'IP类型，HTTP,HTTPS, (HTTP,HTTPS)',
	`submission_date` DATE NOT NULL COMMENT '提交的日期',
	PRIMARY KEY ( `ip_address` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT '记录IP的可用性';
*/


USE parser_component;
DROP TABLE IF EXISTS `IP_availability`;
CREATE TABLE IF NOT EXISTS `IP_availability`(
	`ip_address` VARCHAR(21) NOT NULL COMMENT '主键，ip的地址+端口号，最长可达21位，作为主键可确保数据库中的ip地址不会重复',
	`is_anonymous` BOOLEAN NOT NULL COMMENT '是否为高匿名，是为1，否为0',
	`is_available` BOOLEAN NOT NULL COMMENT '是否仍然可用，是为1，否为0',
	`type` VARCHAR(21) COMMENT 'IP类型，HTTP,HTTPS, (HTTP,HTTPS)',
	`submission_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
	PRIMARY KEY ( `ip_address` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT '记录IP的可用性';




/* --------- user：investor1 ------ */
/* --------- db：parser_component ------ */
/*创建一个表，fake_user_agent，用于存储生成的假UA（用户代理）*/

USE parser_component;
CREATE TABLE IF NOT EXISTS `fake_user_agent`(
	`id` MEDIUMINT NOT NULL AUTO_INCREMENT,
	`ua` VARCHAR(1000) NOT NULL COMMENT '用户代理',
	`submission_date` DATE NOT NULL COMMENT '提交的日期',
	PRIMARY KEY ( `id` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8
COMMENT '生成的假UA（用户代理）';