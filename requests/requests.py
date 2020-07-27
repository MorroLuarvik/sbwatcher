#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль управления запросами """

from datasource import Datasource

class Requests:
    ds = None

    def __init__(self):
        """ инициализация источника данных """
        self.ds = Datasource()

    def get_requests(self):
        """ возвращает массив с запросами """
        fins = self.ds.get_active_finances()
        return fins
