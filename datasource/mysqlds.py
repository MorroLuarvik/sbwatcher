#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль источника данных MySQL """

from .abstractdatasource import AbstractDatasource
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
	def get_finances(self, **where):
		""" получение данных об отслеживаемых финансах """
		query = """
			SELECT
				F.fin_id,
				F.region_id,
				R.region_code,
				R.region_name,
				F.rate_category_id,
				RC.rate_category_code,
				RC.rate_category_name,
				F.curr_id,
				C.curr_code,
				C.curr_iso,
				C.curr_name,
				F.disabled
			FROM f_finances as F
			INNER JOIN s_regions AS R on R.region_id = F.region_id
			INNER JOIN s_rate_categorys AS RC on RC.rate_category_id = F.rate_category_id
			INNER JOIN s_currencys AS C on C.curr_id = F.curr_id
			WHERE %s""" % self._construct_where_conditions(**where)

		cursor = self._get_cursor()

		cursor.execute(query)
		return cursor.fetchall()

	def get_rates(self, **where):
		""" получение истории обменов """
		query = """
			SELECT
				RL.record_id,
				RL.fin_id,
				RL.buy_price,
				RL.sell_price,
				RL.event_ts,
				FROM_UNIXTIME(RL.event_ts) as event_dt,
				F.region_id,
				R.region_code,
				R.region_name,
				F.rate_category_id,
				RC.rate_category_code,
				RC.rate_category_name,
				F.curr_id,
				C.curr_code,
				C.curr_iso,
				C.curr_name,
				F.disabled
			FROM f_rates as RL
			INNER JOIN f_finances as F ON F.fin_id = RL.fin_id
			INNER JOIN s_regions AS R ON R.region_id = F.region_id
			INNER JOIN s_rate_categorys AS RC ON RC.rate_category_id = F.rate_category_id
			INNER JOIN s_currencys AS C ON C.curr_id = F.curr_id
			WHERE %s
			ORDER BY fin_id, event_ts""" % self._construct_where_conditions(**where)

		cursor = self._get_cursor()

		cursor.execute(query)
		return cursor.fetchall()

	def insert_rates(self, values):
		""" добавление параметров в историю обменов """
		query = """
			INSERT INTO f_rates (%s)
			VALUES %s """ % (self._construct_query_keys(values), self._construct_query_values(values))

		cursor = self._get_cursor()

		return cursor.execute(query)

	def _construct_query_keys(self, values):
		""" сборка ключей для функции insert """
		return  ', '.join(values.keys())

	def _construct_query_values(self, values):
		""" сборка значений для функции insert TODO сделать вариант для множества строк"""
		return '(' + ', '.join(str(item) for item in values.values()) + ')'

	def _construct_where_conditions(self, **where):
		""" сборка where условия SQL запроса """
		if len(where) == 0:
			return " 1 = 1 "
		if len(where) == 1 and list(where.values())[0] == None:
			return " 0 = 0 "

		ret_array = []
		for key, val in where.items():
			if isinstance(val, str):
				ret_array.append("%s = '%s'" % (str(key) , str(val)))
				continue

			if misc.isIterable(val):
				ret_array.append("%s in (%s)" % (str(key),  ", ".join(map(str, val))))
				continue
			
			if val is None:
				ret_array.append("%s is null" % str(key))
				continue
			
			ret_array.append("%s = %s" % (str(key) , str(val)))
		
		return " and ".join(ret_array)
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