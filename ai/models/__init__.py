# Rushy Panchal
# ai/models/

from models.rule import Rule

def register(connection):
	'''Register all models with the database'''
	connection.register(Rule)
