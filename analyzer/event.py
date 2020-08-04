#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль финансовых событий """

import datetime

class Event():
	""" Класс финансовых событий """
	fin_id = None
	event_type = None
	rate_id = None
	ds = None

	def __init__(self, ds, fin_id, event_type = 'Ничего', rate_id = 0, event_mode = 'invest'):
		""" инициализация объекта """
		self.fin_id = fin_id
		self.event_type = event_type
		self.rate_id = rate_id
		self.ds = ds

		if not self._is_exists():
			self._register()

	def is_used(self):
		""" кол-во использованных событий """
		return len(self.ds.get_events({'fin_id': self.fin_id, 'rate_id': self.rate_id, 'is_used': 1}))

	def is_suit(self, account = {}):
		""" Подходит ли текущее финансовое событие к аккаунту пользователя """
		if account['curr_volume'] == 0:
			return True
		
		if self.event_type['sell_price'] < account['curr_price']:
			return True
		return False

	def get_fin_id(self):
		""" получение id финанса текущего события  """
		return self.fin_id

	def get_event_type(self):
		""" возвращает описание события """
		return self.event_type

	def set_used(self):
		""" отметка о выполнении """
		return self.ds.update_event({'is_used': True}, {'fin_id': self.fin_id, 'rate_id': self.rate_id})

	def _is_exists(self):
		""" кол-во таких-же событий """
		return len(self.ds.get_events({'fin_id': self.fin_id, 'rate_id': self.rate_id}))

	def _register(self):
		""" кол-во таких-же событий """
		return self.ds.insert_event({'fin_id': self.fin_id, 'rate_id': self.rate_id, 'event_ts': datetime.datetime.now().timestamp()})
