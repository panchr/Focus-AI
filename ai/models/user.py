# Rushy Panchal
# ai/models/user.py

from models.model import Model
from models.auth import HashedPassword

class User(Model):
	'''A single player'''
	__collection__ = "users"

	structure = {
		"display": basestring,
		"email": basestring,
		"password": HashedPassword(), # should be hashed
		"ai": bool,
		}

	required = ["display", "email", "password", "ai"]
