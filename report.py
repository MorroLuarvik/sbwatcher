#!/usr/bin/env python
#-*-coding:utf-8-*-
""" Модуль отправки отчётов """

from configurator.configurator import get_config

smtp_config = get_config("smtp")

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

recepient = "dr.morro.l@gmail.com"

message = MIMEMultipart("alternative")
message["Subject"] = 'Недельный минимум'
message['From'] = smtp_config["login"]["user"]
message['To'] = recepient

message_text = """\
Добрый день.

===================
Проверка с хостинга
===================

Проверка с рабочего компа
Bye!'"""

mail_body = MIMEText(message_text, "plain", "utf-8")

message.attach(mail_body)

smtp_object = smtplib.SMTP(**smtp_config["SMTP"])
smtp_object.login(**smtp_config["login"])
smtp_object.sendmail(smtp_config["login"]["user"], recepient, message.as_string())
smtp_object.quit()

"""
import init

from reports import Manager

rep_manager = Manager()
for rep in rep_manager.get_reports():
	rep.init()
	try:
		rep.send_report()
		rep.confirm_report()
	except Exception as error:
		rep.set_report_error(error)
"""