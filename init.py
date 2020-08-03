#!/usr/bin/env python
#-*-coding:utf-8-*-
""" инициализация модулей """

from datasource import Datasource, MySQL 
from configurator.configurator import get_config

Datasource.register_datasource("mysql", MySQL, get_config("mysql"))

from reports import Manager

Manager.set_report_configs(get_config("smtp"))