#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль получения запросов с внешнего мира """

import init
from misc import PrintException

from requests import Manager

req_manager = Manager()
for req in req_manager.get_requests():
	req.init()
	try:
		req.send_request()
		response, error = req.get_response()
		if not error:
			req.save_response_data(response)
		else:
			req.set_response_error(error)
	except:
		PrintException()
	req.close()