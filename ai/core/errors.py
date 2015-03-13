# Rushy Panchal
# ai/core/errors.py

class WrongPlayerMove(Exception):
	'''Wrong Player is attempting to move'''
	pass

class InvalidMove(Exception):
	'''Attempted move is invalid'''
	pass