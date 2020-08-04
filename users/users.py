#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль управления пользовательскими данными """

from datasource import Datasource

class Users:
	""" Класс управления пользовательскими данными """
	ds = None

	def __init__(self):
		""" инициализация источника данных """
		self.ds = Datasource()
	

	def get_active_accounts(self, fin_id = 0):
		""" возвращает массив с параметрами пользовательских аккаунтов """
		return self.ds.get_accounts({'A.disabled': 0, 'F.disabled': 0, 'A.fin_id': fin_id})