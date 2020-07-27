#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль получения запросов с внешнего мира """

import init

from requests import Manager

import json
import http.client

req_manager = Manager()

for req in req_manager.get_requests():
    connection = http.client.HTTPSConnection(req["host"], req["port"])
    connection.request("GET", req["url"])
    response = connection.getresponse()
    if response.status == 200:
        req_manager.set_response_data(req["id"], json.loads(str(response.read(), 'utf-8')))
    else:
        req_manager.set_response_error(req["id"], response.reason)
    connection.close()
