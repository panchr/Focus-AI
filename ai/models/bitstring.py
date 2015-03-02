# Rushy Panchal
# ai/models/bitstring.py

from models.model import CustomTypeBase
from models.integer import Integer, Long

class Bitstring(CustomTypeBase):
	'''A Custom Type representing a bit string'''
	mongo_type = int
	python_type = Long
	init_type = Long

	def to_bson(self, bitstring):
		'''Converts the Integer to a native int'''
		return bitstring.real

	def to_python(self, value):
		'''Converts a native int to an Integer'''
		return Long(value)
