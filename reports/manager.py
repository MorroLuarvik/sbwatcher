#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль управления запросами """

from datasource import Datasource
from .smtp_report_client import SmtpReportClient
import datetime

class Manager:
	""" Класс управления запросами """
	smtp_config = None

	ds = None
	interface = None

	def __init__(self):
		""" инициализация источника данных """
		self.ds = Datasource()
	
	@classmethod
	def set_report_configs(cls, configs = {} ):
		""" Регистрация конфигурации способа отчёта """
		cls.smtp_config = configs # TODO предусмотреть возможность хранения множества конфигураций

	def get_reports(self):
		""" возвращает массив объектами отчётов """
		# =============== код для проверки всей фигни =============== #
		messages = [
			{
				'report_id': 2,
				'subject': 'Должно приходить сразу',
				'recepient': 'dr.morro.l@gmail.com',
				'message_text': 'Первое сообщение \r\n Вторая строка\r\nБез вывода на экран.'
			},
			{
				'report_id': 42,
				'subject': 'Приходит с опозданием',
				'recepient': 'kozlov-work@yandex.ru',
				'message_text': 'Второе сообщение \r\n Second строка\r\nВывода на экран нет.'
			}
		]
		return [SmtpReportClient(self, row) for row in messages]
		# =============== код для проверки всей фигни =============== #

	def set_report(self, account, event_type):
		""" Формируе сообщение в БД """ 
		recepient = account['user_email']
		subject = account['curr_name'] + ' ' + event_type['type_descr']
		body = """
		{:%Y.%m.%d %H:%M}
		Тип: {}\tВалюта: {}\tЦена: {}
		Это меньше чем {} на вкладе {} с объемом {}.
		""".format(
			datetime.datetime.now(),

			event_type['type_descr'],
			account['curr_name'],
			event_type['sell_price'],

			account['curr_price'],
			account['curr_name'],
			account['curr_volume']
		)
		return self.ds.insert_message({'recepient': recepient, 'subject': subject, 'body': body, 'created_ts': int(datetime.datetime.now().timestamp())})


	def get_smtp_config(self):
		""" возвращает параметры SMTP соединения """
		return self.smtp_config

	def confirm_report_error(self, report_id: int = None):
		""" Подтверждение отправки отчёта """
		# =============== код для проверки всей фигни =============== #
		print("confirm_report_error report_id: {}".format(report_id))
		# =============== код для проверки всей фигни =============== #
		pass
	
	def set_report_error(self, report_id: int = None, error = 'uncknown error'):
		""" Регистрируется ошибка полученная при отправке отчёта """
		# =============== код для проверки всей фигни =============== #
		print("set_report_error report_id: {}, error: \"{}\"".format(report_id, error))
		# =============== код для проверки всей фигни =============== #
		pass
