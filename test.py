#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль проверки кода """

week_date_deep = 24 * 3600 * 7 # неделя
day_date_deep = 24 * 3600 * 1 # неделя

import init
import datetime
from datasource import Datasource

ds = Datasource()
for row in ds.get_rates({'event_ts >': datetime.datetime.now().timestamp() - day_date_deep}):
    row['event_dt_dispaly'] = row['event_dt'].strftime('%Y.%m.%d %H:%M:%S')
    print('{event_dt_dispaly}: \t{curr_name}({fin_id}) \tbuy: {buy_price} \tsell: {sell_price}'.format(**row))

#ss = {'lol': 'sd'}
#print(ds.get_finances({'fin_id <=': 2}))