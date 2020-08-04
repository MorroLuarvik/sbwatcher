#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Загружаем историю торгов """

import init
from datasource import Datasource

ds = Datasource()
for fin_id in [row['fin_id'] for row in ds.get_account_finances({'A.disabled': 0, 'F.disabled': 0})]:
    print(fin_id)

"""
from analyzer import Manager
from users import Users
from reports import reports.Manager
rep_manager = reports.Manager()
users = Users()
an_manager = Manager()


#for fin_id in an_manager.get_active_finances():

for event in an_manager.get_rate_events():
    for account in users.get_active_accounts(fin_id = event.get_fin_id()):
        if event.is_suit(account):
            rep_manager.set_report(account, event)
    event.set_used()
"""