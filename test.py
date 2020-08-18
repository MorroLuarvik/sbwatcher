#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль проверки кода """

import init
import datetime

from reports import Manager as RepManager
rep_manager = RepManager()


print("{:%Y.%m.%d %H:%M}".format(datetime.datetime.now()))

event_type = {'type_name': 'week', 'event_length': 604800, 'sell_price': 58.49, 'type_descr': 'Недельный минимум'}
account = {'rate_category_name': 'Для дистанционных каналов', 'curr_iso': 'Silver', 'fin_id': 2, 'invested_volume': 241.08, 'curr_name': 'Серебро', 'rate_category_id': 1, 'region_code': '27', 'curr_id': 2, 'region_name': 'Хабаровский край', 'curr_volume': 4.0, 'curr_code': 'A99', 'user_alias': 'Morro Luarvik', 'user_email': 'dr.morro.l@gmail.com', 'account_id': 2, 'rate_category_code': 'beznal', 'region_id': 1, 'curr_price': 60.27, 'user_id': 1}

rep_manager.set_report(account, event_type)