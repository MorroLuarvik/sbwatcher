#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль управления запросами """

from datasource import Datasource
from interfaces import Sbrf

class Manager:
		ds = None
		interface = None

		def __init__(self):
				""" инициализация источника данных """
				self.ds = Datasource()
				self.interface = Sbrf(self.ds)

		def get_requests(self):
				""" возвращает массив с запросами """
				fins = self.ds.get_finances(disabled = 0)
				# ============ TODO temporary solution ============ #
				region_code = fins[0]["region_code"]
				rate_category_code = fins[0]["rate_category_code"]

				return self.interface.get_request(0, region_code, rate_category_code, [ fin['curr_code'] for fin in fins ])
				# ============ TODO temporary solution ============ #

		def set_response_data(self, req_id, data):
				""" сохраняет данные для указанного запроса """
				self._save_rates( req_id, self.interface.decode_answer(req_id, data) )

		def set_response_error(self, req_id, error):
				""" регистрируется ошибка при выполнении запроса *не реализовано* TODO """
				pass

		def _save_rates(self, req_id, rate_data):
				""" сохраняет полученные данные """
				for rate_row in rate_data:
						if not self._is_exists_rate(rate_row):
								self.ds.insert_rates(rate_row)
				return True

		def _is_exists_rate(self, rate_row):
				""" проверяет наличие данного курса в истории """
				params = {}
				for key in rate_row.keys():
						params['RL.' + key] = rate_row[key]

				return len(self.ds.get_rates(**params))
