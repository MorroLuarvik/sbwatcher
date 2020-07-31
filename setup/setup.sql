
USE `sbwatcher`;

/*********************************
** географические регионы       **
*********************************/
DROP TABLE IF EXISTS  `sbwatcher`.`s_regions`;
CREATE TABLE `sbwatcher`.`s_regions` (
    `region_id`  int unsigned NOT NULL primary key AUTO_INCREMENT,
    `region_code` VARCHAR (8) NOT NULL DEFAULT '',
    `region_name` VARCHAR (256),

    UNIQUE KEY `region_code_idx` (`region_code`) USING BTREE,
    KEY `region_name_idx` (`region_name`) USING BTREE
) ENGINE=InnoDB ROW_FORMAT=DYNAMIC DEFAULT CHARSET=utf8;

INSERT INTO `sbwatcher`.`s_regions` (`region_code`, `region_name`)
VALUES ('27', 'Хабаровский край');

/*********************************
** типы обменов                 **
*********************************/
DROP TABLE IF EXISTS  `sbwatcher`.`s_rate_categorys`;
CREATE TABLE `sbwatcher`.`s_rate_categorys` (
    `rate_category_id`  int unsigned NOT NULL primary key AUTO_INCREMENT,
    `rate_category_code` VARCHAR (16) NOT NULL DEFAULT '',
    `rate_category_name` VARCHAR (256),

    UNIQUE KEY `rate_category_code_idx` (`rate_category_code`) USING BTREE,
    KEY `rate_category_name_idx` (`rate_category_name`) USING BTREE
) ENGINE=InnoDB ROW_FORMAT=DYNAMIC DEFAULT CHARSET=utf8;

INSERT INTO `sbwatcher`.`s_rate_categorys` (`rate_category_code`, `rate_category_name`)
VALUES ('beznal', 'Для дистанционных каналов');

/*********************************
** валюты                       **
*********************************/
DROP TABLE IF EXISTS  `sbwatcher`.`s_currencys`;
CREATE TABLE `sbwatcher`.`s_currencys` (
    `curr_id`  int unsigned NOT NULL primary key AUTO_INCREMENT,
    `curr_code` VARCHAR (16) NOT NULL DEFAULT '',
    `curr_iso` VARCHAR (16) NOT NULL DEFAULT '',
    `curr_name` VARCHAR (256),

    UNIQUE KEY `curr_code_idx` (`curr_code`) USING BTREE,
    KEY `curr_iso_idx` (`curr_iso`) USING BTREE,
    KEY `curr_name_idx` (`curr_name`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO `sbwatcher`.`s_currencys` (`curr_code`, `curr_iso`, `curr_name`)
VALUES 
    ('840', 'USD', 'Доллар США'),
    ('A99', 'Silver', 'Серебро'),
    ('A33', 'palladium', 'Палладий');

/*********************************
** отслеживаемые финансы        **
*********************************/
DROP TABLE IF EXISTS  `sbwatcher`.`f_finances`;
CREATE TABLE `sbwatcher`.`f_finances` (
    `fin_id`  int unsigned NOT NULL primary key AUTO_INCREMENT,
    `region_id` int unsigned NOT NULL,
    `rate_category_id` int unsigned NOT NULL,
    `curr_id`  int unsigned NOT NULL,
    `disabled` TINYINT UNSIGNED NOT NULL DEFAULT 0,

    UNIQUE KEY `fin_idx` (`region_id`, `rate_category_id`, `curr_id`) USING BTREE,
    KEY `region_idx` (`region_id`) USING BTREE,
    KEY `rate_category_idx` (`rate_category_id`) USING BTREE,
    KEY `curr_idx` (`curr_id`) USING BTREE,
    KEY `disabled_idx` (`disabled`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO `sbwatcher`.`f_finances` (`region_id`, `rate_category_id`, `curr_id`)
VALUES 
    (1, 1, 1),
    (1, 1, 2),
    (1, 1, 3);

/*********************************
** логи курсов                  **
*********************************/
DROP TABLE IF EXISTS  `sbwatcher`.`f_rates`;
CREATE TABLE `sbwatcher`.`f_rates` (
    `record_id`  int unsigned NOT NULL primary key AUTO_INCREMENT,
    `fin_id` int unsigned NOT NULL,
    `buy_price` FLOAT (16,2) unsigned NOT NULL,
    `sell_price` FLOAT (16,2) UNSIGNED NOT NULL,
    `event_ts`  int unsigned NOT NULL,

    UNIQUE KEY `rate_idx` (`fin_id`, `event_ts`) USING BTREE,
    KEY `fin_idx` (`fin_id`) USING BTREE,
    KEY `buy_price_idx` (`buy_price`) USING BTREE,
    KEY `sell_price_idx` (`sell_price`) USING BTREE,
    KEY `event_ts_idx` (`event_ts`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*********************************
** пользователи системы         **
*********************************/
DROP TABLE IF EXISTS  `sbwatcher`.`u_users`;
CREATE TABLE `sbwatcher`.`u_users` (
    `user_id`  int unsigned NOT NULL primary key AUTO_INCREMENT,
    `user_email` VARCHAR (255) NOT NULL DEFAULT '',
    `user_alias` VARCHAR (255),

    UNIQUE KEY `user_email_idx` (`user_email`) USING BTREE,
    KEY `user_alias_idx` (`user_alias`) USING BTREE
) ENGINE=InnoDB ROW_FORMAT=DYNAMIC DEFAULT CHARSET=utf8;

INSERT INTO `sbwatcher`.`u_users` (`user_email`, `user_alias`)
VALUES ('dr.morro.l@gmail.com', 'Morro Luarvik');

/*********************************
** финансы пользоватеелй        **
*********************************/
DROP TABLE IF EXISTS  `sbwatcher`.`u_accounts`;
CREATE TABLE `sbwatcher`.`u_accounts` (
    `account_id` int unsigned NOT NULL primary key AUTO_INCREMENT,
    `user_id` int unsigned NOT NULL,
    `fin_id` int unsigned NOT NULL,
    `curr_volume` FLOAT (16,8) unsigned NOT NULL,
    `invested_volume` FLOAT (16,2) unsigned NOT NULL,
    `curr_price` FLOAT (16,2) UNSIGNED NOT NULL,
    `disabled` TINYINT UNSIGNED NOT NULL DEFAULT 0,

    UNIQUE KEY `account_idx` (`user_id`, `fin_id`) USING BTREE,
    KEY `user_idx` (`user_id`) USING BTREE,
    KEY `fin_idx` (`fin_id`) USING BTREE,
    KEY `curr_volume_idx` (`curr_volume`) USING BTREE,
    KEY `invested_volume_idx` (`invested_volume`) USING BTREE,
    KEY `curr_price_idx` (`curr_price`) USING BTREE,
    KEY `disabled_idx` (`disabled`) USING BTREE
) ENGINE=InnoDB ROW_FORMAT=DYNAMIC DEFAULT CHARSET=utf8;

/*********************************
** События для анализа          **
*********************************/
DROP TABLE IF EXISTS  `sbwatcher`.`a_events`;
CREATE TABLE `sbwatcher`.`a_events` (
    `event_id` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `event_name` VARCHAR (127) NOT NULL DEFAULT '',
    `event_param` VARCHAR (127) DEFAULT '',
    
    UNIQUE KEY `event_name_idx` (`event_param`) USING BTREE
) ENGINE=InnoDB ROW_FORMAT=DYNAMIC DEFAULT CHARSET=utf8;

INSERT INTO `sbwatcher`.`a_events` (`event_name`, `event_param`)
VALUES
    ('Недельный минимум', CONVERT(3600 * 24 * 7, CHAR)),
    ('Двухнедельный минимум', CONVERT(3600 * 24 * 14, CHAR)),
    ('Месячный минимум', CONVERT(3600 * 24 * 30, CHAR)),
    ('Квартальный минимум', CONVERT(3600 * 24 * 30, CHAR)),
    ('Плугодовой минимум', CONVERT(3600 * 24 * 30, CHAR)),
    ('Годовой минимум', CONVERT(3600 * 24 * 365, CHAR));


/*********************************
** шаблоны отчётов              **
*********************************/
DROP TABLE IF EXISTS  `sbwatcher`.`r_templates`;
CREATE TABLE `sbwatcher`.`r_templates` (
    `template_id`  int unsigned NOT NULL primary key AUTO_INCREMENT,
    `tempalte_subject` VARCHAR (255) NOT NULL DEFAULT '',
    `template_body` TEXT,

    UNIQUE KEY `tempalte_subject_idx` (`tempalte_subject`) USING BTREE,
    KEY `template_body_idx` (`template_body`(255)) USING BTREE
) ENGINE=InnoDB ROW_FORMAT=DYNAMIC DEFAULT CHARSET=utf8;

