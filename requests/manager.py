#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль управления запросами """

from datasource import Datasource
from interfaces import Sbrf
from .https_request_client import HttpsRequestClient

class Manager:
		ds = None
		interface = None

		def __init__(self):
				""" инициализация источника данных """
				self.ds = Datasource()
				self.ds.switch_datasource('request')
				self.interface = Sbrf(self.ds)

		def get_requests(self):
				""" возвращает массив с запросами """
				fins = self.ds.get_finances({'disabled =': 0})
				# ============ TODO temporary solution ============ #
				#region_code = fins[0]["region_code"]
				#rate_category_code = fins[0]["rate_category_code"]

				return [ HttpsRequestClient(self, params) 
					for params in (
						self.interface.get_request_params(fin["fin_id"], fin["region_code"], fin["rate_category_code"], [fin["curr_code"]]) 
							for fin in fins
					) 
				]
				#return self.interface.get_request_params(0, region_code, rate_category_code, [ fin['curr_code'] for fin in fins ])
				# ============ TODO temporary solution ============ #

		def set_response_data(self, request_params, data):
				""" сохраняет данные для указанного запроса """
				self._save_rates( request_params["id"], self.interface.decode_answer(request_params, data) )

		def set_response_error(self, req_id, error):
				""" регистрируется ошибка при выполнении запроса *не реализовано* TODO """
				raise Exception("Ошибка \"%s\" при выполении запроса %n" %  error, req_id)

		def _save_rates(self, req_id, rate_data):
				""" сохраняет полученные данные """
				for rate_row in rate_data:
						if not self.ds.is_exists_rate(rate_row):
							self.ds.insert_rates(rate_row)
				return True
