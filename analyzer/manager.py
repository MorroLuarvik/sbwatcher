#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль управления событиями """

import datetime
from datasource import Datasource
from .event import Event

class Manager:
	""" Класс управления событиями """

	event_types = [
		{
			'type_name': 'year',
			'type_descr': 'Годовой минимум',
			'event_length': 3600 * 24 * 365
		},
		{
			'type_name': 'half_year',
			'type_descr': 'Полугодовой минимум',
			'event_length': 3600 * 12 * 365
		},
		{
			'type_name': 'three_months',
			'type_descr': 'Квартальный минимум',
			'event_length': 3600 * 24 * 90
		},
		{
			'type_name': 'month',
			'type_descr': 'Месячный минимум',
			'event_length': 3600 * 24 * 30
		},
		{
			'type_name': 'two_weeks',
			'type_descr': 'Двухнедельный минимум',
			'event_length': 3600 * 24 * 14
		},
		{
			'type_name': 'week',
			'type_descr': 'Недельный минимум',
			'event_length': 3600 * 24 * 7
		}
	]

	ds = None

	def __init__(self):
		""" инициализация источника данных """
		self.ds = Datasource()
		self.ds.switch_datasource('stat')
	

	def get_rate_events(self):
		""" возвращает массив с объектами событий """
		events = []
		for fin_id in [row['fin_id'] for row in self.ds.get_account_finances({'A.disabled': 0, 'F.disabled': 0})]:
			event_type, rate_id = self._get_invest_event(fin_id)
			if (event_type is not None):
				events.append(Event(self.ds, fin_id, event_type, rate_id, 'invest'))	
			event_type, rate_id = self._get_profit_event(fin_id)
			if (event_type is not None):
				events.append(Event(self.ds, fin_id, event_type, rate_id, 'profit'))	
		return events

	def _get_invest_event(self, fin_id: int = 0):
		""" Определяет финансовое событие инвестирования и возвращает event_type, rate_id """
		try:
			[rate_row] = self.ds.get_top_rate({'RL.fin_id': fin_id})
		except ValueError:
			return None, None

		for event_type in self.event_types:
			start_ts = datetime.datetime.now().timestamp() - event_type['event_length']
			[state_row] = self.ds.get_stat_rates({'fin_id': fin_id, 'event_ts >': start_ts})
			if state_row['min_sell_price'] >= rate_row['sell_price']:
				event_type['sell_price'] = rate_row['sell_price']
				return event_type, rate_row['rate_id']

		return None, None
	
	def _get_profit_event(self, fin_id: int = 0):
		""" Определяет финансовое событие профита и возвращает event_type, rate_id """
		try:
			[rate_row] = self.ds.get_top_rate({'RL.fin_id': fin_id})
		except ValueError:
			return None, None
		
		price_change = self.ds.get_change_percent(fin_id)
		if price_change > 0:
			return None, None
		
		event_type = {
			'type_name': 'downtrend',
			'type_descr': 'Нисходящий тренд',
			'event_length': 666,
			'sell_price': rate_row['sell_price'],
			'buy_price': rate_row['buy_price'],
			'price_change': price_change
		}

		return 	event_type, rate_row['rate_id']

	def set_report_error(self, report_id: int = None, error = 'uncknown error'):
		""" Регистрируется ошибка полученная при отправке отчёта """
		# =============== код для проверки всей фигни =============== #
		print("set_report_error report_id: {}, error: \"{}\"".format(report_id, error))
		# =============== код для проверки всей фигни =============== #
		pass
