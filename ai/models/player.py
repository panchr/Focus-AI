# Rushy Panchal
# ai/models/player.py

from models.model import Model
from models.auth import HashedPassword

class Player(Model):
	'''A single player'''
	structure = {
		"display": basestring,
		"email": basestring,
		"password": HashedPassword, # should be hashed
		"ai": bool,
		}

	required = ["display", "email", "password", "ai"]
