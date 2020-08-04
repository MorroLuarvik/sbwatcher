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
	def get_finances(self, where = {}):
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
			WHERE %s""" % self._construct_where_conditions(where)

		cursor = self._get_cursor()

		cursor.execute(query)
		return cursor.fetchall()

	def get_rates(self, where = {}):
		""" получение истории обменов """
		query = """
			SELECT
				RL.rate_id,
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
			ORDER BY fin_id, event_ts""" % self._construct_where_conditions(where)

		cursor = self._get_cursor()

		cursor.execute(query)
		return cursor.fetchall()
	
	def get_top_rate(self, where = {}):
		""" получение последнего обмена """
		query = """
			SELECT
				RL.rate_id,
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
			ORDER BY fin_id, event_ts DESC
			LIMIT 1""" % self._construct_where_conditions(where)

		cursor = self._get_cursor()

		cursor.execute(query)
		return cursor.fetchall()

	def get_stat_rates(self, where = {}):
		""" получение статистики обменов """
		query = """
			SELECT
				fin_id,
				MIN(buy_price) AS min_buy_pice,
				MAX(buy_price) AS max_buy_pice,
				AVG(buy_price) AS avg_buy_pice,
				MIN(sell_price) AS min_sell_pice,
				MAX(sell_price) AS max_sell_pice,
				AVG(sell_price) AS avg_sell_pice
			FROM f_rates
			WHERE %s
			GROUP BY fin_id""" % self._construct_where_conditions(where)

		cursor = self._get_cursor()

		cursor.execute(query)
		return cursor.fetchall()

	def is_exists_rate(self, where = {}):
		""" наличие записи в истории обменов """
		params = {}
		for key in where.keys():
				params['RL.' + key] = where[key]

		return len(self.get_rates(params))

	def insert_rates(self, values):
		""" добавление параметров в историю обменов """
		query = """
			INSERT INTO f_rates (%s)
			VALUES %s """ % (self._construct_query_keys(values), self._construct_query_values(values))

		cursor = self._get_cursor()

		return cursor.execute(query)

	def get_accounts(self, where = {}):
		""" получение списка текущих аккаунтов """
		query = """
			SELECT
				A.account_id,
				A.user_id,
				U.user_email,
				U.user_alias,
				A.fin_id,
				c.curr_iso,
				A.curr_volume,
				A.invested_volume,
				A.curr_price,
				F.region_id,
				R.region_code,
				R.region_name,
				F.rate_category_id,
				RC.rate_category_code,
				RC.rate_category_name,
				F.curr_id,
				c.curr_code,
				c.curr_name
			FROM u_accounts AS A
			INNER JOIN u_users AS U ON u.user_id = A.user_id
			INNER JOIN f_finances AS F ON F.fin_id = A.fin_id
			INNER JOIN s_regions AS R ON R.region_id = R.region_id
			INNER JOIN s_rate_categorys AS RC ON RC.rate_category_id = F.rate_category_id
			INNER JOIN s_currencys AS C On F.curr_id = c.curr_id
			WHERE %s""" % self._construct_where_conditions(where)

		cursor = self._get_cursor()

		cursor.execute(query)
		return cursor.fetchall()

	def get_account_finances(self, where = {}):
		""" получение списка финансов текущих аккаунтов """
		query = """
			SELECT DISTINCT
				A.fin_id,
				F.region_id,
				R.region_code,
				R.region_name,
				F.rate_category_id,
				RC.rate_category_code,
				RC.rate_category_name,
				F.curr_id,
				c.curr_code,
				c.curr_iso,
				c.curr_name
			FROM u_accounts AS A
			INNER JOIN f_finances AS F ON F.fin_id = A.fin_id
			INNER JOIN s_regions AS R ON R.region_id = R.region_id
			INNER JOIN s_rate_categorys AS RC ON RC.rate_category_id = F.rate_category_id
			INNER JOIN s_currencys AS C On F.curr_id = c.curr_id
			WHERE %s
			GROUP BY fin_id""" % self._construct_where_conditions(where)

		cursor = self._get_cursor()

		cursor.execute(query)
		return cursor.fetchall()

	def get_events(self, where = {}):
		""" получение списка событий """
		query = """
			SELECT 
				event_id,
				fin_id,
				rate_id,
				event_ts,
				is_used
			FROM a_events
			WHERE %s""" % self._construct_where_conditions(where)

		cursor = self._get_cursor()

		cursor.execute(query)
		return cursor.fetchall()
	
	def insert_event(self, values):
		""" добавление события """
		query = """
			INSERT INTO a_events (%s)
			VALUES %s """ % (self._construct_query_keys(values), self._construct_query_values(values))

		cursor = self._get_cursor()

		cursor.execute(query)
		return self.connect.commit()

	def update_event(self, values, where):
		""" изменение события """
		query = """
			UPDATE a_events 
			SET %s
			WHERE %s """ % (self._construct_query_sets(values), self._construct_where_conditions(where))

		print(query)

		cursor = self._get_cursor()

		cursor.execute(query)
		return self.connect.commit()

	def _construct_query_keys(self, values):
		""" сборка ключей для функции insert """
		return  ', '.join(values.keys())

	def _construct_query_values(self, values):
		""" сборка значений для функции insert TODO сделать вариант для множества строк"""
		return '(' + ', '.join(str(item) for item in values.values()) + ')'

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