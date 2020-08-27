#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль источника данных MySQL c информацией об отчётах """

from .wrap_ds import MySQL

class Report(MySQL):
	""" Источник данных MySQL c информацией об отчётах """
	
	def get_messages(self, where = {}):
		""" получение списка сообщений """
		query = """
			SELECT 
				message_id,
				recepient,
				subject,
				body,
				created_ts,
				send_ts
			FROM r_messages
			WHERE %s""" % self._construct_where_conditions(where)

		cursor = self._get_cursor()

		cursor.execute(query)
		return cursor.fetchall()
	
	def insert_message(self, values):
		""" добавление сообщения """
		query = """
			INSERT INTO r_messages (%s)
			VALUES %s """ % (self._construct_query_keys(values), self._construct_query_values(values))

		cursor = self._get_cursor()

		cursor.execute(query)
		return self.connect.commit()
	
	def update_message(self, values, where):
		""" изменение сообщения """
		query = """
			UPDATE r_messages 
			SET %s
			WHERE %s """ % (self._construct_query_sets(values), self._construct_where_conditions(where))

		cursor = self._get_cursor()

		cursor.execute(query)
		return self.connect.commit()
