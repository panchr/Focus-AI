# Rushy Panchal
# ai/models/state.py

from models.model import CustomTypeBase

class Gamestate(CustomTypeBase):
	'''Depicts the game state

	BSON representation: 01,02,03|11,12,13|21,22,23
	Python representation: [
		[01, 02, 03],
		[11, 12, 13],
		[21, 22, 23]
		]

	Each individual element is stored as an integer'''

	mongo_type = basestring
	python_type = [list]
	init_type = [list]

	@classmethod
	def new(cls, width = 8, height = 8):
		'''Creates a new Game state descriptor'''
		return [[0] * height for w in xrange(width)]

	def to_bson(self, value):
		'''Converts the Python object to a BSON representation'''
		return "|".join(",".join(map(str, part)) for part in value)

	def to_python(self, value):
		'''Converts the BSON representation to a Python object'''
		return [map(int, part.split(",")) for part in value.split("|")]
