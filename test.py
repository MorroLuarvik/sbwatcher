#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль проверки кода """

import init
from datasource import Datasource

ds = Datasource()
for row in ds.get_rates():
    print(row)
