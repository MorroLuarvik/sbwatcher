#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль проверки кода """

import init
from misc import PrintException

try:
    a = 3
    b = 0
    print(a/b)
except:
    PrintException()