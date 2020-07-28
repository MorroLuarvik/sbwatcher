#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль проверки кода """

import init

from datasource import Datasource
from interfaces import Sbrf

interface = Sbrf(Datasource())
print(interface._get_fin_id(27, 'beznal', 840))