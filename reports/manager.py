#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль управления запросами """

from datasource import Datasource
from .smtp_report_client import SmtpReportClient

class Manager:

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
			return []

		def get_smtp_config(self):
			""" возвращает параметры SMTP соединения """
			return self.smtp_config

		def confirm_report_error(self, report_id: int = None):
			""" Подтверждение отправки отчёта """
			pass
		
		def set_report_error(self, report_id: int = None, error = 'uncknown error'):
			""" Регистрируется ошибка полученная при отправке отчёта """
			pass
