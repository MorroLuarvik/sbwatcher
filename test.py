#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль проверки кода """

import init

import datetime
from datasource import Datasource

DDD = 24 * 3600

ds = Datasource()

def get_middle_price(fin_id, start_ts, end_ts):
    [rate_stat] = ds.get_stat_rates({'event_ts >=': start_ts, 'event_ts <=': end_ts, 'fin_id': fin_id})
    return (rate_stat['avg_sell_price'] + rate_stat['avg_buy_price']) / 2

def get_change_percent(fin_id):
    now_ts = datetime.datetime.now().timestamp()
    base_price = get_middle_price(fin_id, now_ts - DDD * 10, now_ts * DDD * 3)
    new_price = get_middle_price(fin_id, now_ts - DDD * 7, now_ts)
    return 100 - new_price * 100 / base_price

for fin_row in ds.get_finances({'disabled =': 0}):
    [top_rate] = ds.get_top_rate({'RL.fin_id': fin_row['fin_id']})
    top_rate['event_dt_dispaly'] = top_rate['event_dt'].strftime('%Y.%m.%d %H:%M:%S')
    top_rate['change_percent'] = get_change_percent(fin_row['fin_id'])
    print("{event_dt_dispaly} {curr_name} \tbuy: {buy_price} \tsell: {sell_price}\tchange percent: {change_percent:+05.2f}%".format(**top_rate))