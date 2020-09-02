#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль источника данных MySQL cо статистической информацией """

from .wrap_ds import MySQL
import datetime

class Stat(MySQL):
	""" Источник данных MySQL cо статистической информацией """
	
	SECONDS_IN_DAY = 3600 * 24

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
				MIN(buy_price) AS min_buy_price,
				MAX(buy_price) AS max_buy_price,
				AVG(buy_price) AS avg_buy_price,
				MIN(sell_price) AS min_sell_price,
				MAX(sell_price) AS max_sell_price,
				AVG(sell_price) AS avg_sell_price
			FROM f_rates
			WHERE %s
			GROUP BY fin_id""" % self._construct_where_conditions(where)

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
				C.curr_code,
				C.curr_iso,
				C.curr_name
			FROM u_accounts AS A
			INNER JOIN f_finances AS F ON F.fin_id = A.fin_id
			INNER JOIN s_regions AS R ON R.region_id = R.region_id
			INNER JOIN s_rate_categorys AS RC ON RC.rate_category_id = F.rate_category_id
			INNER JOIN s_currencys AS C On F.curr_id = C.curr_id
			WHERE %s
			GROUP BY fin_id""" % self._construct_where_conditions(where)

		cursor = self._get_cursor()

		cursor.execute(query)
		return cursor.fetchall()
	
	def get_middle_price(self, fin_id, start_ts, end_ts):
		""" получить среднюю цену за указанный период """
		[rate_stat] = self.get_stat_rates({'event_ts >=': start_ts, 'event_ts <=': end_ts, 'fin_id': fin_id})
		return (rate_stat['avg_sell_price'] + rate_stat['avg_buy_price']) / 2

	def get_change_percent(self, fin_id, len_in_days = 7, deep_in_days = 10):
		""" получить изменение цены в % за период deep_in_days, средняя цена берётся за период len_in_days """
		now_ts = datetime.datetime.now().timestamp()
		base_price = self.get_middle_price(fin_id, now_ts - self.SECONDS_IN_DAY * deep_in_days, now_ts - self.SECONDS_IN_DAY * (deep_in_days - len_in_days))
		new_price = self.get_middle_price(fin_id, now_ts - self.SECONDS_IN_DAY * len_in_days, now_ts)
		return new_price * 100 / base_price - 100

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

		cursor = self._get_cursor()

		cursor.execute(query)
		return self.connect.commit()