#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Разные полезные функции """

import time
import linecache
import sys

def TStoStr(ts = 0, format = "%Y.%m.%d %H:%M:%S"):
	""" Перевод unix timestamp в строку """
	return time.strftime(format, time.localtime(ts))

def StrToTS(strTime = "2018.09.01 00:00:00", format = "%Y.%m.%d %H:%M:%S"):
	""" Перевод строки в unix timestamp """
	return int(time.mktime(time.strptime(strTime, format)))

def ceil(i, n=0):
	""" Отбрасываем дробную часть """ 
	return int(i * 10 ** n) / float(10 ** n)

def isIterable(obj):
	""" Проверяем на итерируемость """
	try:
		_ = (e for e in obj)
	except Exception:
		return False
	else:
		return True	

def PrintException():
    _, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('Exception in ({}, line {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
