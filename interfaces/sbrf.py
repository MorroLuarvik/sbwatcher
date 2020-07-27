#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль интерфейса сайта сбербанка """

class Sbrf:
    """ Интерфейс сайта сбербанка """
   
    host = "www.sberbank.ru"
    base_url = "/portalserver/proxy/?pipe=shortCachePipe&url=http%3A%2F%2Flocalhost%2Frates-web%2FrateService%2Frate%2Fcurrent%3F"
    port = 443

    def get_request(self, request_id = None, region_code = "27", rate_category_code = "beznal", curr_codes = []):
        # ============ TODO temporary solution ============ #
        region = "regionId%3D" + region_code
        rate_category = "rateCategory%3D" + rate_category_code
        return [{
            "id": 0,
            "host": self.host,
            "url": self.base_url + "%26".join([region, rate_category] + ["currencyCode%3D" + curr_code for curr_code in curr_codes]),
            "port": self.port}]
        # ============ TODO temporary solution ============ #
