# Rushy Panchal
# ai/models/response.py

from models.model import CustomTypeBase

class Response(CustomTypeBase):
	'''A Custom type representing a Dynamic Scripting response'''
	mongo_type = basestring
	python_type = basestring
	init_type = None

	# similar to the condition, there is no actual interpretation of the response (just yet)
	# it will be implemented in the future as I work on the AI and figure out how it is structured
