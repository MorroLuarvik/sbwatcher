#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль финансовых событий """

class Event():
	""" Класс финансовых событий """
	fin_id = None
	ds = None

	def __init__(self, ds, fin_id, event_type = 'Ничего', rate_id = 0, event_mode = 'invest'):
		""" инициализация объекта """
		self.fin_id = fin_id
		self.ds = ds

	def is_used(self):
		""" True - если такое событие существует и уже использовано """
		return False

	def get_fin_id(self):
		""" получение id финанса текущего события  """
		return self.fin_id


	def set_used(self):
		""" отметка о выполнении """
		pass
