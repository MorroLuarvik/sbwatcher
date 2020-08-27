#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль проверки кода """

import sys

DEFAULT_DAYS = 1

#print(len(sys.argv))

days = DEFAULT_DAYS

if len(sys.argv) > 1:
    try:
        days = int(sys.argv[1])
    except ValueError:
        days = DEFAULT_DAYS


print(days)