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
        print(req_id, data)
        pass

    def set_response_error(self, req_id, error):
        print(req_id, error)
        pass