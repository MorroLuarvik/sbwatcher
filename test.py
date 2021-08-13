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
"""

Datasource.register_datasource("request", Request, get_config("mysql"))
ds = Datasource()
ds.switch_datasource('request')
interface = Sbrf(ds)

fins = ds.get_finances({'disabled =': 0})

for fin in fins:
    print(fin['curr_name'])
    request_param = interface.get_request_params(fin["fin_id"], fin["region_code"], fin["rate_category_code"], [curr_codes for curr_codes in [fin["curr_code"]]])

    connection = http.client.HTTPSConnection(host, port)
    connection.request("GET", request_param["url"])

    response = connection.getresponse()
    if response.status == 200:
        print("success")
        data = json.loads(str(response.read(), 'utf-8'))
        print(data)
    else:
        print("error")
        print(response.reason)
        exit()

    #print(data.keys())

    region_code = interface._get_region_code_by_req(request_param["id"])

    for curr_code in data.keys():
        row = {}
        row = {"fin_id": interface._get_fin_id(region_code, request_param["rateCategoryCode"], curr_code)}
        row.update( interface._get_rate_row(data[curr_code]) )
        idx = 0 # idx - min amount, станешь богатым учтёшь этот момент
        row.update( interface._get_rate_row(data[curr_code]["rateList"][idx]) )
        print(row)

        """
        for curr_code in data[rate_category_code].keys():
            print(curr_code)
        """

    #print("Region code: {}".format( interface._get_region_code_by_req(request_params["id"]) ) )
    #print(list(fin["curr_code"]))


#print( [ {"lol": fin['curr_name'], "kek": interface.get_request_params(fin["fin_id"], fin["region_code"], fin["rate_category_code"], [fin["curr_code"]]) } for fin in fins ] )


print('second')

