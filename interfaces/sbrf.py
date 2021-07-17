#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль интерфейса сайта сбербанка """

class Sbrf:
	""" Интерфейс сайта сбербанка """
   
	host = "www.sberbank.ru"
	base_url = "/proxy/services/rates/public/actual?"
	port = 443

	data_relations = {
		'rateBuy': 'buy_price', 
		'rateSell': 'sell_price', 
		'activeFrom': 'event_ts'
	}

	ds = None

	def __init__(self, ds = None):
		self.ds = ds
		self.ds.switch_datasource('request')

	def get_request_params(self, req_id = 0, region_code = "038", rate_category_code = None, curr_codes = []):
		""" получить структура запроса к серверу """
		# ============ TODO temporary solution ============ #
		region = "regionId=" + region_code
		rate_category = "rateType=" + rate_category_code
		return [{
			"id": req_id,
			"host": self.host,
			"url": self.base_url + "&".join( [region, rate_category] + [ "isoCodes[]=" + curr_code for curr_code in curr_codes ] ),
			"port": self.port}]
		# ============ TODO temporary solution ============ #

	def decode_answer(self, req_id = None, data = {}):
		""" декодирование ответа сервера в терминах текущей БД """
		region_code = self._get_region_code_by_req(req_id)
		ret = []
		for rate_category_code in data.keys():
			for curr_code in data[rate_category_code].keys():
				idx = '0' # idx - min amount, станешь богатым учтёшь этот момент
				if idx in data[rate_category_code][curr_code]:
					row = {"fin_id": self._get_fin_id(region_code, rate_category_code, curr_code)}
					row.update( self._get_rate_row(data[rate_category_code][curr_code][idx]) )
					ret.append(row)
		return ret

	def _get_fin_id(self, region_code, rate_category_code, curr_code):
		""" получить id финансов из текущей БД TODO """
		return self.ds.get_finances({'region_code =': region_code, 'rate_category_code =': rate_category_code, 'curr_code =': curr_code})[0]['fin_id']

	
	def _get_rate_row(self, row_data = {}):
		""" приведение строки к виду БД """
		ret = { self.data_relations[key]: row_data[key] for key in self.data_relations.keys() if key in row_data.keys() }
		ret['event_ts'] = int(ret['event_ts'] / 1000)
		return ret


	def _get_region_code_by_req(self, req_id):
		""" возвращает code региона по номеру запроса """
		return '038'        