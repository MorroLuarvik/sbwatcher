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

for event in an_manager.get_rate_event(fin_id):
    for account in users.get_active_account(fin_id = event.get_fin_id()):
        if an_manager.is_suit(account, event):
            rep_manager.send_report(account, event)
    an_manager.set_used(event)
"""