#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль проверки кода """

import init

from requests import Requests

rr = Requests()
print(rr.get_requests())
