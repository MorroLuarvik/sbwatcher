#!/usr/bin/env python
#-*-coding:utf-8-*-
""" инициализация модулей """

from datasource import Datasource, MySQL 
from datasource import Users
from datasource import Request
from datasource import Report
from datasource import Stat

from configurator.configurator import get_config

Datasource.register_datasource("mysql", MySQL, get_config("mysql"))
Datasource.register_datasource("users", Users, get_config("mysql"))
Datasource.register_datasource("request", Request, get_config("mysql"))
Datasource.register_datasource("report", Report, get_config("mysql"))
Datasource.register_datasource("stat", Stat, get_config("mysql"))

from reports import Manager

Manager.set_report_configs(get_config("smtp"))