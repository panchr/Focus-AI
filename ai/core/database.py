# Rushy Panchal
# ai/core/database.py

import pymongo

class Database(pymongo.Connection):
	'''Specific database wrapper for a MongoDB database'''
	def setup(self, path = "setup.sql", models = None):
		'''Sets up the database'''
		if not models:
			models = []
		for model in models:
			self.register(model)
