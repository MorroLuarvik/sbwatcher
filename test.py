#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль проверки кода """

import init

dr = {
    "a": "aa", 
    "b": "bb",
    "c": "xx"
}

row = {"a": 4, "b": -32, 'z': 42 }

print( {dr[key]: row[key] for key in dr.keys() if key in row.keys()} )
