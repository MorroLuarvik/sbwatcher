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
        for rate_category_code in data.keys():
            for curr_code in data[rate_category_code].keys():
                for idx in data[rate_category_code][curr_code]:
                    self._save_rate( req_id, self.interface.decode_answer(req_id, data[rate_category_code][curr_code][idx]) )

        print(req_id, data)
        pass

    def set_response_error(self, req_id, error):
        """ регистрируется ошибка при выполнении запроса *не реализовано* """
        pass

    def _save_rate(self, req_id, data):
        """ сохраняет полученные данные """
        if self._is_exists_rate(region_id, curr_code, rate_dict):
            return False

        return True

    def _is_exists_rate(self, region_id, curr_code, rate_dict):
        """ проверяет наличие данного курса в истории """

    def _get_region_by_req(self, req_id):
        """ возвращает id региона по номеру запроса """
        return 1