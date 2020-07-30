#!/usr/bin/env python
#-*-coding:utf-8-*-
""" https клиент """

from .abstract_request_client import AbstractRequestClient

import json
import http.client

class HttpsRequestClient(AbstractRequestClient):
	""" Абстрактный класс отправки запросов """
	req_source = None
	request_params = None
	connection = None

	def __init__(self, req_source, request_params):
		""" инициализация объекта """
		self.req_source = req_source
		self.request_params = request_params

	def init(self):
		""" Инициализация соединения """
		self.connection = http.client.HTTPSConnection(self.request_params["host"], self.request_params["port"])
	
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
		self.req_source.set_response_data(self.request_params["id"], json.loads(str(response.read(), 'utf-8')))

	def set_response_error(self, error):
		""" Сохранение ошибки в источнике данных """
		self.req_source.set_response_error(self.request_params["id"], error)
	
	def close(self):
		""" Закрытие соединения """
		self.connection.close()
