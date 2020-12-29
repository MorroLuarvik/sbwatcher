#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль отправки отчётов """

import init

from reports import Manager

rep_manager = Manager()
for rep in rep_manager.get_reports():
	rep.init()
	try:
		rep.send_report()
		rep.confirm_report()
	except Exception as error:
		rep.set_report_error(error)
	rep.close()
	#break