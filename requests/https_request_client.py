#!/usr/bin/env python
#-*-coding:utf-8-*-
""" https клиент """

from .abstract_request_client import AbstractRequestClient

import json
import http.client
import ssl

class HttpsRequestClient(AbstractRequestClient):
	""" Абстрактный класс отправки запросов """
	req_manager = None
	request_params = None
	connection = None

	def __init__(self, req_manager, request_params):
		""" инициализация объекта """
		self.req_manager = req_manager
		self.request_params = request_params

	def init(self):
		""" Инициализация соединения """
		self.connection = http.client.HTTPSConnection(self.request_params["host"], self.request_params["port"], context = ssl._create_unverified_context())
	
	def send_request(self):
		""" Отправка запроса объекта """
		self.connection.request("GET", self.request_params["url"])

	def get_response(self):
		""" Получение ответа в виде JSON, error_message """
		self.response = self.connection.getresponse()
		if self.response.status == 200:
			return json.loads(str(self.response.read(), 'utf-8')), False
		else:
			return {}, self.response.reason

	def save_response_data(self, response):
		""" Сохранение ответа в источнике данных """
		self.req_manager.set_response_data(self.request_params, response)

	def set_response_error(self, error):
		""" Сохранение ошибки в источнике данных """
		self.req_manager.set_response_error(self.request_params["id"], error)
	
	def close(self):
		""" Закрытие соединения """
		self.connection.close()
