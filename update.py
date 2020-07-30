#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Загружаем историю торгов """

import sys
import init
from datasource import Datasource
ds = Datasource()

if len(sys.argv) != 3:
	print("Укажите fin_id и файл с исходниками торгов: \"update.py fin_id source_file\"")
	for row in ds.get_finances({'disabled =': 0}):
		print("{rate_category_name} \t{curr_name}: \t{fin_id}".format(**row))
	quit()

fin_id = int(sys.argv[1])
if len(ds.get_finances({'disabled =': 0, 'fin_id =': fin_id})) != 1:
	print("В БД нет записи fin_id = {}".format(fin_id))
	quit()

import os

file_name = str(sys.argv[2])
if not os.path.isfile(file_name):
	print("Не найден файл \"{}\"".format(file_name))
	quit()

import json

rates_file = open(file_name, 'r+')
rates = json.load(rates_file)
rates_file.close()

[fin_info] = ds.get_finances({'disabled =': 0, 'fin_id =': fin_id})

if fin_info['curr_code'] not in rates:
	print("Ошибка curr_code. Неправильный формат файла \"{}\"".format(file_name))
	quit()

if 'rates' not in rates[fin_info['curr_code']]:
	print("Ошибка rates. Неправильный формат файла \"{}\"".format(file_name))
	quit()

from interfaces import Sbrf
sbr = Sbrf(ds)

print("Процесс пошёл")
prev_event_ts = 0
for rate_row in rates[fin_info['curr_code']]['rates']:
	row = {'fin_id': fin_id}
	row.update(sbr._get_rate_row(rate_row))
	if not ds.is_exists_rate(row) and row['event_ts'] != prev_event_ts:
		ds.insert_rates(row)
	prev_event_ts = row['event_ts']
print("Процесс окончен")