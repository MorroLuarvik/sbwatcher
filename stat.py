#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль проверки кода """

import init

from datasource import Datasource

ds = Datasource()
ds.switch_datasource('stat')

for fin_row in ds.get_finances({'disabled =': 0}):
    [top_rate] = ds.get_top_rate({'RL.fin_id': fin_row['fin_id']})
    top_rate['event_dt_dispaly'] = top_rate['event_dt'].strftime('%Y.%m.%d %H:%M:%S')
    top_rate['change_percent'] = ds.get_change_percent(fin_row['fin_id'])
    print("{event_dt_dispaly} {curr_name} \tbuy: {buy_price} \tsell: {sell_price}\tchange percent: {change_percent:+05.2f}%".format(**top_rate))
