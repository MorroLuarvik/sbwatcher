#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль проверки кода """

import init

try:
    s = 1 / 0
except Exception as error:
    print(error)