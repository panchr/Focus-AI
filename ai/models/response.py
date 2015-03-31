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

	def to_python(self, value):
		'''Convert the value to a Python object

		This is required because Numpy index accesses require tuples'''
		if len(value) < 2 or len(value[1]) == 0 or isinstance(value[1][0], int):
			return map(tuple, value)
		else:
			return [tuple(value[0]), map(tuple, value[1])]

	@classmethod
	def new(cls):
		'''Creates a new Response'''
		return [(), ()] # return an empty 2-D list (no move)
