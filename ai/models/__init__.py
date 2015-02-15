# Rushy Panchal
# ai/models/

from models.rule import Rule
from models.user import User

def register(connection):
	'''Register all models with the database'''
	connection.register(Rule)
	connecton.register(User)
