#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль отображения текущей информации """

SECONDS_IN_DAY = 24 * 3600 * 1
DEFAULT_DAYS = 1

import init
import sys
import datetime
from datasource import Datasource

days = DEFAULT_DAYS

if len(sys.argv) > 1:
    try:
        days = int(sys.argv[1])
    except ValueError:
        days = DEFAULT_DAYS


ds = Datasource()
ds.switch_datasource('stat')
for row in ds.get_rates({'event_ts >': datetime.datetime.now().timestamp() - days * SECONDS_IN_DAY}):
    row['event_dt_dispaly'] = row['event_dt'].strftime('%Y.%m.%d %H:%M:%S')
    print('{event_dt_dispaly} {curr_name} \tbuy: {buy_price} \tsell: {sell_price}'.format(**row))
