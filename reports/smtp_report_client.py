#!/usr/bin/env python
#-*-coding:utf-8-*-
""" https клиент """

from .abstract_report_client import AbstractReportClient

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SmtpReportClient(AbstractReportClient):
	""" Абстрактный класс отправки запросов """
	rep_manager = None
	report_params = None
	
	smtp_config = None
	message = MIMEMultipart("alternative")

	def __init__(self, rep_manager, report_params):
		""" инициализация объекта """
		self.rep_manager = rep_manager
		self.report_params = report_params
		
		self.smtp_config = self.rep_manager.get_smtp_config()

	def init(self):
		""" Подготовка отчёта """
		self.message["Subject"] = self.report_params['subject']
		self.message['From'] = self.smtp_config["login"]["user"]
		self.message['To'] = self.report_params['recepient']

		mail_body = MIMEText(self.report_params['body'], "plain", "utf-8")
		self.message.attach(mail_body)


	def send_report(self):
		""" Отправка отчёта """
		self.smtp_object = smtplib.SMTP(**self.smtp_config["SMTP"])
		self.smtp_object.login(**self.smtp_config["login"])
		self.smtp_object.sendmail(self.smtp_config["login"]["user"], self.report_params['recepient'], self.message.as_string())
		#print(self.message.as_string())

	def confirm_report(self):
		""" Подтверждение отправки отчёта """
		self.rep_manager.confirm_report_error(self.report_params["message_id"])

	def set_report_error(self, error):
		""" Сохранение ошибки в источнике данных """
		self.rep_manager.set_report_error(self.report_params["message_id"], error)
	
	def close(self):
		""" Закрытие соединения """
		self.smtp_object.quit()
