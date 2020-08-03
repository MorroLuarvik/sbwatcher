#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Структура отправки отчётов """

class AbstractReportClient:
	""" Абстрактный класс отправки отчётов """

	def init(self):
		""" Инициализация объекта """
		raise NotImplementedError("Определите init в %s." % (self.__class__.__name__))
	
	def send_report(self):
		""" Отправка отчёта """
		raise NotImplementedError("Определите send_report в %s." % (self.__class__.__name__))

	def confirm_report(self):
		""" Подтверждение отправки отчёта """
		raise NotImplementedError("Определите confirm_report в %s." % (self.__class__.__name__))

	def set_report_error(self, error):
		""" Сохранение ошибки в источнике данных """
		raise NotImplementedError("Определите set_response_error в %s." % (self.__class__.__name__))
	
	def close(self):
		""" Закрытие соединения """
		raise NotImplementedError("Определите close в %s." % (self.__class__.__name__))