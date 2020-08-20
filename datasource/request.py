#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль источника данных MySQL c информацией о запросах """

from .mysqlds import MySQL

class Request(MySQL):
	""" Источник данных MySQL c информацией о запросах """
	
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
	
