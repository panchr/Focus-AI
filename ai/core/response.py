# Rushy Panchal
# app/controllers/response.py

import json
import arrow

class Response(object):
	'''A class containing all response types'''
	@staticmethod
	def error(error, **data): # needs unit tests
		'''Returns a JSON response for an error'''
		return Response.json(error.message, error.errorMessage, error.errorCode, **data)

	@staticmethod
	def json(message, status, code = None, timestamp = None, **data):
		'''Returns a standard JSON response'''
		if code is None:
			code = status if isinstance(status, int) else 200
		response = {
			"message": message,
			"status": status,
			"type": code,
			"timestamp": timestamp or arrow.utcnow().isoformat()
			}
		response.update(data)
		return response # not encoded in json
