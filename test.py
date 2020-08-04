#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль проверки кода """

import init

from analyzer import Manager
a_manager = Manager()

print(a_manager._get_event(2))