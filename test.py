#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль проверки кода """

import init

from datasource import Datasource

ds = Datasource()

print(ds.datasource_list)
print(ds.selected_datasource)
ds.switch_datasource('mysql')
print(ds.datasource_list)
print(ds.selected_datasource)
ds.switch_datasource('users')
print(ds.datasource_list)
print(ds.selected_datasource)