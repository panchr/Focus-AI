# Rushy Panchal
# ai/models/condition.py

from models.model import CustomTypeBase

class Condition(CustomTypeBase):
	'''A Custom type representing a Dynamic Scripting condition'''
	mongo_type = basestring
	python_type = basestring
	init_type = basestring

	# as of now, there is no actual interpretation of the condition
	# That will be implemented once I start the actual AI and figure out exactly how the conditions are structured
	# So, the mongo/python types are likely to change in the future
