#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль интерфейса сайта сбербанка """

class Sbrf:
	""" Интерфейс сайта сбербанка """
   
	host = "www.sberbank.ru"
	base_url = "/portalserver/proxy/?pipe=shortCachePipe&url=http%3A%2F%2Flocalhost%2Frates-web%2FrateService%2Frate%2Fcurrent%3F"
	port = 443

	data_relations = {
		'buyValue': 'buy_price', 
		'sellValue': 'sell_price', 
		'activeFrom': 'event_ts'
	}

	ds = None

	def __init__(self, ds = None):
		self.ds = ds
		self.ds.switch_datasource('request')

	def get_request_params(self, req_id = None, region_code = "27", rate_category_code = "beznal", curr_codes = []):
		""" получить структура запроса к серверу """
		# ============ TODO temporary solution ============ #
		region = "regionId%3D" + region_code
		rate_category = "rateCategory%3D" + rate_category_code
		return [{
			"id": 0,
			"host": self.host,
			"url": self.base_url + "%26".join( [region, rate_category] + [ "currencyCode%3D" + curr_code for curr_code in curr_codes ] ),
			"port": self.port}]
		# ============ TODO temporary solution ============ #

	def decode_answer(self, req_id = None, data = {}):
		""" декодирование ответа сервера в терминах текущей БД """
		region_code = self._get_region_code_by_req(req_id)
		ret = []
		for rate_category_code in data.keys():
			for curr_code in data[rate_category_code].keys():
				#for idx in data[rate_category_code][curr_code]:
				idx = '0' 
				if idx in data[rate_category_code][curr_code]:
					#print('key inside')
					#print(data[rate_category_code][curr_code][idx])
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
		return '27'        