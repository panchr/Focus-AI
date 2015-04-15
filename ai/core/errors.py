# Rushy Panchal
# ai/core/errors.py

class WrongPlayerMove(Exception):
	'''Wrong Player is attempting to move'''
	pass

class InvalidMove(Exception):
	'''Attempted move is invalid'''
	pass

class BaseError(Exception):
	'''Base error class that every exception should inherit from'''
	errorCode = 500
	errorMessage = "Something went wrong"

class MalformedQuery(BaseError):
	'''Query was malformed'''
	errorCode = 400
	errorMessage = "Bad request"

class NotFound(BaseError):
	'''Document not found error'''
	errorCode = 404
	errorMessage = "Not found"
