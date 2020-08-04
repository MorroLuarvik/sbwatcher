#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль проверки кода """

import init
import datetime

from datasource import Datasource

ds = Datasource()
print(ds.get_events())
ds.insert_event({'fin_id': 0, 'rate_id': 666, 'event_ts': datetime.datetime.now().timestamp()})
#print(ds.get_events())
ds.update_event({'is_used': True}, {'fin_id': 0, 'rate_id': 666})
print(ds.get_events())

"""
exit()

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
            print(account)
            #rep_manager.set_report(account, event)
    #event.set_used()
"""