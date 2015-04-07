# Rushy Panchal
# ai/models/model.py

import mongokit

import config

class Model(mongokit.Document, object):
	'''Base class for all Models'''
	__database__ = config.DB_NAME

	use_dot_notation = True
	skip_validation = True

	connection = None

	def __init__(self, *args, **kwargs):
		'''Wrapper to the mongokit.Document.__init__'''
		super(Model, self).__init__(*args, **kwargs)
		self.collection = Model.connection[self.__database__][self.__collection__]

	@classmethod
	def new(cls, **values):
		'''Create a new object in the database'''
		o = cls.connection[cls.__name__]
		o.update(values)
		o.save()
		return o

	@staticmethod
	def autosave(func):
		'''Returns a decorated function to add implicit saving'''
		def decorated(self, *args, **kwargs):
			shouldSave = False
			saveProvided = "save" in kwargs
			# autosave if user wants to save OR if no save parameter provided
			if ((saveProvided and kwargs["save"]) or not saveProvided):
				shouldSave = True
			if saveProvided:
				del kwargs["save"]
			returnValue = func(self, *args, **kwargs)
			if shouldSave:
				self.save()
			return returnValue
		return decorated

class CustomTypeBase(mongokit.CustomType, object):
	'''Base class for a custom Mongokit type'''
	mongo_type = None
	python_type = None
	init_type = None

	def to_bson(self, value):
		'''Converts Python object to BSON'''
		return value

	def to_python(self, value):
		'''Converts BSON to a Python object'''
		return value
