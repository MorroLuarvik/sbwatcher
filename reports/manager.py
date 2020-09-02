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
		self.ds.switch_datasource('report')
	
	@classmethod
	def set_report_configs(cls, configs = {} ):
		""" Регистрация конфигурации способа отчёта """
		cls.smtp_config = configs # TODO предусмотреть возможность хранения множества конфигураций

	def get_reports(self):
		""" возвращает массив объектами отчётов """
		messages = self.ds.get_messages({'send_ts': None})
		return [SmtpReportClient(self, row) for row in messages]

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

	def confirm_report_error(self, message_id: int = None):
		""" Подтверждение отправки отчёта """
		return self.ds.update_message({'send_ts': int(datetime.datetime.now().timestamp())}, {'message_id': message_id})
	
	def set_report_error(self, report_id: int = None, error = 'uncknown error'):
		""" Регистрируется ошибка полученная при отправке отчёта """
		# =============== код для проверки всей фигни =============== #
		print("set_report_error report_id: {}, error: \"{}\"".format(report_id, error))
		# =============== код для проверки всей фигни =============== #
		pass
