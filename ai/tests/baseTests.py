# Rushy Panchal
# tests/baseTest.py

import types

dev = True

CALLABLE_TYPES = (
	types.FunctionType,
	types.LambdaType,
	types.MethodType,
	)

class BaseTest(object):
	'''A collection of general unit testing'''
	def assertHasAttr(self, o, attr):
		'''Object has an attribute'''
		self.assertTrue(hasattr(o, attr), "{o} does not have attribute {attr}".format(o = o, attr = attr))
	
	def assertIsSubclass(self, child, parent):
		'''Child is subclass of parent'''
		self.assertTrue(issubclass(child, parent), "{child} is not a subclass of {parent}".format(child = child, parent = parent))

	def assertFunctionExists(self, o, functionName):
		'''functionName exists and is a callable function'''
		self.assertHasAttr(o, functionName)
		self.assertIsInstance(getattr(o, functionName), CALLABLE_TYPES)

	def flattenDict(self, dictionary, base = ""):
		'''Flatten a dictionary to extract all of the keys'''
		values = dictionary.keys()
		if (base):
			values = map(lambda item: base + "." + item, values)
		for (k, d) in dictionary.iteritems():
			if (isinstance(d, dict)):
				values.extend(self.flattenDict(d, k))
		return values

	def accessFlattened(self, dictionary, key):
		'''Access the key of a flattened dictionary value set'''
		splitted = key.split(".", 1)
		if (len(splitted) > 1):
			return self.accessFlattened(dictionary[splitted[0]], splitted[1])
		else:
			return dictionary[key]