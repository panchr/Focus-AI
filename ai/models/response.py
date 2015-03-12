# Rushy Panchal
# ai/models/response.py

from models.model import CustomTypeBase

class Response(CustomTypeBase):
	'''A Custom type representing a Dynamic Scripting response

	The response is structured as a 2-D list:
		[old position, new position]'''
	mongo_type = list
	python_type = list
	init_type = list

	@classmethod
	def new(cls):
		'''Creates a new Response'''
		return [(), ()] # return an empty 2-D list (no move)
