# Rushy Panchal
# ai/models/model.py

import mongokit

class Model(object, mongokit.Document):
	'''Base class for all Models'''
	__database__ = "senior_focus"
	__collection__ = ""

	use_dot_notation = True
	skip_validation = True
