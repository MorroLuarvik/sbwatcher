#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль проверки кода """

import json
import http.client

from datasource import Datasource
from datasource import Request
from configurator.configurator import get_config
from interfaces import Sbrf

print("begin")

host = "www.sberbank.ru"
port = 443

url = "/proxy/services/rates/public/actual?rateType=PMR-3&isoCodes[]=A99&regionId=038" # металлы
#url = "/proxy/services/rates/public/actual?rateType=ERNP-2&isoCodes[]=USD&regionId=038" # валюта

# ERNP-2 валюта в сбер-онлайн

"""
connection = http.client.HTTPSConnection(host, port)
connection.request("GET", url)

response = connection.getresponse()
if response.status == 200:
    print("success")
    print(str(response.read(), 'utf-8'))
else:
    print("error")
    print(response.reason)
"""

Datasource.register_datasource("request", Request, get_config("mysql"))
ds = Datasource()
ds.switch_datasource('request')
interface = Sbrf(ds)

fins = ds.get_finances({'disabled =': 0})

for fin in fins:
    print(fin['curr_name'])
    print( interface.get_request_params(fin["fin_id"], fin["region_code"], fin["rate_category_code"], [fin["curr_code"]]) )


print( [ {fin['curr_name'], interface.get_request_params(fin["fin_id"], fin["region_code"], fin["rate_category_code"], [fin["curr_code"]]) } for fin in fins ] )


print('second')

