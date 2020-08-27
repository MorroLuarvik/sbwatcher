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

	def get_account_finances(self, where = {}):
		""" получение списка финансов текущих аккаунтов """
		raise NotImplementedError("Определите get_account_finances в %s." % (self.__class__.__name__))

	def get_accounts(self, where = {}):
		""" получение списка текущих аккаунтов """
		raise NotImplementedError("Определите get_accounts в %s." % (self.__class__.__name__))

	def get_events(self, where = {}):
		""" получение списка событий """
		raise NotImplementedError("Определите get_events в %s." % (self.__class__.__name__))
	
	def get_messages(self, where = {}):
		""" получение списка сообщений """
		raise NotImplementedError("Определите get_messages в %s." % (self.__class__.__name__))

	def insert_event(self, values):
		""" добавление события """
		raise NotImplementedError("Определите insert_event в %s." % (self.__class__.__name__))
	
	def insert_message(self, values):
		""" добавление сообщения """
		raise NotImplementedError("Определите insert_message в %s." % (self.__class__.__name__))

	def update_event(self, values, where):
		""" изменение события """
		raise NotImplementedError("Определите update_event в %s." % (self.__class__.__name__))
	
	def update_message(self, values, where):
		""" изменение сообщения """
		raise NotImplementedError("Определите update_message в %s." % (self.__class__.__name__))

