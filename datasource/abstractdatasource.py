#!/usr/bin/env python
#-*-coding:utf-8-*-

class AbstractDatasource:
	""" Абстрактный источник данных """

	def get_finances(self, **where):
		""" Список отслеживаемых финансов """
		raise NotImplementedError("Определите get_exchange в %s." % (self.__class__.__name__))
