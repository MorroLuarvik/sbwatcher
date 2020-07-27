#!/usr/bin/env python
#-*-coding:utf-8-*-

from .abstractdatasource import AbstractDatasource
from mysql import connector
import misc

class MySQL(AbstractDatasource):
	""" Источник данных MySQL """

	connect = None

	def __init__(self, host = None, db = None, user = None, password = None, port = 3306):
		""" инициализация источника данных """
		self.connect = connector.connect(
			host = host,
			user = user,
			password = password,
			db = db,
			port = port,
			charset = 'utf8',
			use_unicode = True)

	# ----------------------------- реализация функций абстрактного класса ----------------------------- #
	def get_active_finances(self, disabled = 0):
		""" получение списка активных финансов """
		query = """
			SELECT 
				F.fin_id,
				F.region_id,
				R.region_code,
				F.rate_category_id,
				RC.rate_category_code,
				F.curr_id,
				C.curr_code
			FROM 
				f_finances as F
			INNER JOIN
				s_regions AS R on R.region_id = F.region_id
			INNER JOIN
				s_rate_categorys AS RC ON RC.rate_category_id = F.rate_category_id
			INNER JOIN
				s_currencys AS C ON C.curr_id = F.curr_id
			WHERE
				F.disabled = %s
			ORDER BY region_code, rate_category_id;
		""" % (disabled)

		cursor = self.connect.cursor(dictionary = True)

		cursor.execute(query)
		return cursor.fetchall()

	def _construct_where_conditions(self, **where):
		""" сборка where условия SQL запроса """
		if len(where) == 0:
			return " 1 = 1 "
		if len(where) == 1 and list(where.values())[0] == None:
			return " 0 = 0 "

		ret_array = []
		for key, val in where.items():
			if misc.isIterable(val):
				ret_array.append("%s in (%s)" % (str(key),  ", ".join(map(str, val))))
				continue
			
			if val is None:
				ret_array.append("%s is null" % str(key))
				continue
			
			ret_array.append("%s = %s" % (str(key) , str(val)))
		
		return " and ".join(ret_array)
	# ----------------------------- реализация функций абстрактного класса ----------------------------- #

	def __del__(self):
		if self.connect.is_connected():
			self.connect.close()
