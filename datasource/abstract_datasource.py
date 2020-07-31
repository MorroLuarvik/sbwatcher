#!/usr/bin/env python
#-*-coding:utf-8-*-

class AbstractDatasource:
	""" Абстрактный источник данных """

	def get_finances(self, where = {}):
		""" Список отслеживаемых финансов """
		raise NotImplementedError("Определите get_exchange в %s." % (self.__class__.__name__))
	
	def get_rates(self, where = {}):
		""" получение истории обменов """
		raise NotImplementedError("Определите get_exchange в %s." % (self.__class__.__name__))
	
	def get_top_rate(self, where = {}):
		""" получение последнего обмена """
		raise NotImplementedError("Определите get_exchange в %s." % (self.__class__.__name__))

	def get_stat_rates(self, where = {}):
		""" получение статистики обменов """
		raise NotImplementedError("Определите get_exchange в %s." % (self.__class__.__name__))

	def is_exists_rate(self, where = {}):
		""" наличие записи в истории обменов """
		raise NotImplementedError("Определите get_exchange в %s." % (self.__class__.__name__))

	def insert_rates(self, values = {}):
		""" добавление параметров в историю обменов """
		raise NotImplementedError("Определите get_exchange в %s." % (self.__class__.__name__))

