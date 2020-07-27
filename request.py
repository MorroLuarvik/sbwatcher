#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль получения запросов с внешнего мира """

import init

from requests import RequestManager

import json
import http.client

host = "www.sberbank.ru"
url = "/portalserver/proxy/?pipe=shortCachePipe&url=http%3A%2F%2Flocalhost%2Frates-web%2FrateService%2Frate%2Fcurrent%3FregionId%3D77%26rateCategory%3Dbeznal%26currencyCode%3D840"
port = 443

req_manager = RequestManager()

for req in req_manager.get_requests():
    connection = http.client.HTTPSConnection(req["host"], req["port"])
    connection.request("GET", req["url"])
    response = connection.getresponse()
    if response.status == 200:
        req_manager.set_response_data(req["id"], json.loads(str(response.read(), 'utf-8')))
    else:
        req_manager.set_response_error(req["id"], response.reason)
    connection.close()
