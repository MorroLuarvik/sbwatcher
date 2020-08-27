#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль источника данных MySQL """

from .abstract_datasource import AbstractDatasource
try:
	# normal system
	from mysql import connector as connector
except ImportError:
	# reduced system
	import MySQLdb as connector
import misc

class MySQL(AbstractDatasource):
	""" Источник данных MySQL """

	connect = None

	def __init__(self, host = None, db = None, user = None, password = None, port = 3306):
		""" инициализация источника данных """
		params = {
			"host": host,
			"user": user,
			"password": password,
			"db": db,
			"port": port,
			"charset": 'utf8',
			"use_unicode": True
		}

		if connector.__name__ != 'mysql.connector':
			params["passwd"] = password
			del(params["password"])

		self.connect = connector.connect(**params)

	# ----------------------------- реализация функций абстрактного класса ----------------------------- #
	def _construct_query_keys(self, values):
		""" сборка ключей для функции insert """
		return  ', '.join(values.keys())

	def _construct_query_values(self, values):
		""" сборка значений для функции insert TODO сделать вариант для множества строк"""
		return '(' + ', '.join('"' + str(item) + '"' for item in values.values()) + ')'

	def _construct_where_conditions(self, where = {}):
		""" сборка where условия SQL запроса """
		if len(where) == 0:
			return " 1 = 1 "

		ret_array = []
		for key, val in where.items():
			compare_sign = '='
			if ' ' in key:
				[key, compare_sign] = key.split(' ')
			if isinstance(val, str):
				ret_array.append("%s %s '%s'" % (str(key), compare_sign,  str(val)))
				continue

			if misc.isIterable(val):
				ret_array.append("%s in (%s)" % (str(key),  ", ".join(map(str, val))))
				continue
			
			if val is None:
				ret_array.append("%s is null" % str(key))
				continue
			
			ret_array.append("%s %s %s" % (str(key), compare_sign, str(val)))
		
		return " and ".join(ret_array)
	
	def _construct_query_sets(self, values):
		""" сборка SET выражения для UPDATE """
		ret_array = []
		for key, val in values.items():
			if isinstance(val, str):
				ret_array.append("%s = '%s'" % (str(key), str(val)))
				continue
			
			if val is None:
				ret_array.append("%s = null" % str(key))
				continue
			
			ret_array.append("%s = %s" % (str(key), str(val)))
		
		return ", ".join(ret_array)
	# ----------------------------- реализация функций абстрактного класса ----------------------------- #

	def _get_cursor(self):
		""" получение курсовра """
		try:
			cursor = self.connect.cursor(dictionary = True)
		except TypeError:
			cursor = self.connect.cursor(connector.cursors.DictCursor)
		return cursor

	def __del__(self):
		""" закрываем соединение """
		try:
			is_connected = self.connect.is_connected()
		except AttributeError:
			is_connected = self.connect.ping(True)
		if is_connected:
			self.connect.close()