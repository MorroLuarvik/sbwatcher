#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Структура отправки запросов """

class AbstractRequestClient:
	""" Абстрактный класс отправки запросов """

	def init(self):
		""" Инициализация объекта """
		raise NotImplementedError("Определите init в %s." % (self.__class__.__name__))
	
	def send_request(self):
		""" Отправка запроса объекта """
		raise NotImplementedError("Определите send_request в %s." % (self.__class__.__name__))

	def get_response(self):
		""" Получение ответа в виде JSON, error_message """
		raise NotImplementedError("Определите get_response в %s." % (self.__class__.__name__))

	def save_response_data(self, response):
		""" Сохранение ответа в источнике данных """
		raise NotImplementedError("Определите save_response_data в %s." % (self.__class__.__name__))

	def set_response_error(self, error):
		""" Сохранение ошибки в источнике данных """
		raise NotImplementedError("Определите set_response_error в %s." % (self.__class__.__name__))
	
	def close(self):
		""" Закрытие соединения """
		raise NotImplementedError("Определите close в %s." % (self.__class__.__name__))