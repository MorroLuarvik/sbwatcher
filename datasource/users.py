#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль источника данных MySQL c информацией о пользователях """

from .mysqlds import MySQL

class Users(MySQL):
	""" Источник данных MySQL c информацией о пользователях """
	
	def get_accounts(self, where = {}):
		""" получение списка текущих аккаунтов """
		query = """
			SELECT
				A.account_id,
				A.user_id,
				U.user_email,
				U.user_alias,
				A.fin_id,
				C.curr_iso,
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
				C.curr_code,
				C.curr_name
			FROM u_accounts AS A
			INNER JOIN u_users AS U ON U.user_id = A.user_id
			INNER JOIN f_finances AS F ON F.fin_id = A.fin_id
			INNER JOIN s_regions AS R ON R.region_id = R.region_id
			INNER JOIN s_rate_categorys AS RC ON RC.rate_category_id = F.rate_category_id
			INNER JOIN s_currencys AS C On F.curr_id = C.curr_id
			WHERE %s""" % self._construct_where_conditions(where)

		cursor = self._get_cursor()

		cursor.execute(query)
		return cursor.fetchall()


