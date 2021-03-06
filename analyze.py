#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Загружаем историю торгов """

import init

from analyzer import Manager as AnManager
an_manager = AnManager()
from users import Users
users = Users()
from reports import Manager as RepManager
rep_manager = RepManager()


for event in an_manager.get_rate_events():
	if event.is_used():
		continue
	for account in users.get_active_accounts(fin_id = event.get_fin_id()):
		if event.is_suit(account):
			rep_manager.set_report(account, event.get_event_type())
	event.set_used()
