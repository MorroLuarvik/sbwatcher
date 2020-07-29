#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль проверки кода """

import init
from datasource import Datasource

ds = Datasource()
for row in ds.get_rates():
    row['event_dt_dispaly'] = row['event_dt'].strftime('%Y.%m.%d %H:%M:%S')
    print('{event_dt_dispaly}: \t{curr_name}({fin_id}) \tbuy: {buy_price} \tsell: {sell_price}'.format(**row))
