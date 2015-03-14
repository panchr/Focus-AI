# Rushy Panchal
# ai/models/

from models.model import Model
from models.user import User
from models.rule import Rule
from models.game import Game

def register(connection):
	'''Register the connection with all of the models'''
	Model.connection = connection
