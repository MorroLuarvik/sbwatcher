#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль получения запросов с внешнего мира """

import json
import http.client

host = "www.sberbank.ru"
url = "/portalserver/proxy/?pipe=shortCachePipe&url=http%3A%2F%2Flocalhost%2Frates-web%2FrateService%2Frate%2Fcurrent%3FregionId%3D77%26rateCategory%3Dbeznal%26currencyCode%3D840"
port = 443

connection = http.client.HTTPSConnection(host, port)
connection.request("GET", url)
response = connection.getresponse()
print("Status: %d and reason: %s" % (response.status, response.reason))
if response.status == 200:
    data = json.loads(str(response.read(), 'utf-8'))
    print(data)
connection.close()
