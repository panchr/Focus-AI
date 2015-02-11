# Rushy Panchal
# ai/models/auth.py

import bcrypt

from models.model import CustomTypeBase

class HashedPassword(CustomTypeBase):
	'''MongoDB Model for storing (and authenticating) user passwords'''
	mongo_type = basestring
	python_type = basestring
	init_type = basestring

	@staticmethod
	def new(password = ""):
		'''Hashes a new password'''
		return HashedPassword.hash(password)

	@staticmethod
	def check(password, hashed):
		'''Checks if the password matches the hashed password'''
		return (bcrypt.hashpw(password, hashed) == hashed)

	@staticmethod
	def hash(password, salt = ""):
		'''Hashes a password'''
		return bcrypt.hashpw(password, bcrypt.gensalt() if not salt else salt)
