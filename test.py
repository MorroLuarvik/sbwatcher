#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль проверки кода """

import init

from datasource import Datasource

ds = Datasource()

print(ds.get_stat_rates({'fin_id': [1, 2]}))

print("привет!")