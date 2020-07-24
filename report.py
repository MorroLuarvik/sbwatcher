#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль отправки отчётов """

from configurator.configurator import get_config

import smtplib

recepient = "dr.morro.l@gmail.com"

message = """\
From: work computer <from@fromdomain.com>
To: To Person <%s>
MIME-Version: 1.0
Content-type: text/plain; charset=utf-8
Subject: need 2 read

This is an e-mail message to be sent in HTML format

WO "u" symbol in start string 
""" % (recepient)

smtp_config = get_config("smtp")

smtpObj = smtplib.SMTP(**smtp_config["SMTP"])
smtpObj.login(**smtp_config["login"])
smtpObj.sendmail(smtp_config["login"]["user"], recepient, message)
smtpObj.quit()
