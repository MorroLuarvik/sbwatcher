#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль управления запросами """

from datasource import Datasource

class RequestManager:
    host = "www.sberbank.ru"
    base_url = "/portalserver/proxy/?pipe=shortCachePipe&url=http%3A%2F%2Flocalhost%2Frates-web%2FrateService%2Frate%2Fcurrent%3F"
    port = 443

    ds = None

    def __init__(self):
        """ инициализация источника данных """
        self.ds = Datasource()

    def get_requests(self):
        """ возвращает массив с запросами """
        fins = self.ds.get_active_finances()
        # ============ TODO temporary solution ============ #
        region = "regionId%3D" + fins[0]["region_code"]
        rate_category = "rateCategory%3D" + fins[0]["rate_category_code"]
        return [{
            "id": 0,
            "host": self.host,
            "url": self.base_url + "%26".join([region, rate_category] + ["currencyCode%3D" + d['curr_code'] for d in fins]),
            "port": self.port}]
        # ============ TODO temporary solution ============ #

    def set_response_data(self, req_id, data):
        region_id = self._get_region_by_req(req_id)
        for rate_category_code in data.keys():
            for curr_code in data[rate_category_code].keys():
                for idx in data[rate_category_code][curr_code]:
                    self._save_rate(
                            region_id, 
                            curr_code,
                            data[rate_category_code][curr_code][idx])

        print(req_id, data)
        pass

    def set_response_error(self, req_id, error):
        """ регистрируется ошибка при выполнении запроса *не реализовано* """
        pass

    def _save_rate(self, region_id, curr_code, rate_dict):
        """ сохраняет полученные данные """
        if self._is_exists_rate(region_id, curr_code, rate_dict):
            return False

        return True

    def _is_exists_rate(self, region_id, curr_code, rate_dict):
        """ проверяет наличие данного курса в истории """

    def _get_fin_id(self, region_id, curr_code, rate_dict):
        """ возвращает fin_id по указанным параметрам для сбера """

    def _get_region_by_req(self, req_id):
        """ возвращает id региона по номеру запроса """
        return 1