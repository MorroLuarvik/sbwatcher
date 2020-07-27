#!/usr/bin/env python
#-*-coding:utf-8-*-

class AbstractDatasource:
	""" Абстрактный источник данных """

	def get_active_finances(self, disabled = 0):
		""" Список активных финансов """
		raise NotImplementedError("Определите get_exchange в %s." % (self.__class__.__name__))
