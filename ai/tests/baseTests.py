# Rushy Panchal
# tests/baseTest.py

import types
import unittest
import numpy as np

dev = True

TEST_HOST = 'localhost'
TEST_PORT = 27017

CALLABLE_TYPES = (
	types.FunctionType,
	types.LambdaType,
	types.MethodType,
	)

class BaseTest(object):
	'''A collection of general unit testing'''
	def test_inheritsTestcase(self):
		'''Tests that the test case inherits from unittest.TestCase'''
		self.assertIsInstance(self, unittest.TestCase)

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

class NumpyTest(BaseTest):
	'''A wrapper around BaseTest that also allows for Numpy Array testing'''
	def assertEquals(self, a, b):
		'''Asserts that two objects are equal'''
		if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
			self.assertArrayEquals(a, b)
		else:
			super(BaseTest, self).assertEquals(a, b)

	def assertInArray(self, element, array):
		'''Asserts that element is in the array'''
		for x in array:
			if (element == x).all():
				return True
		self.fail("{element} not found in {array}".format(element = element, array = array))

	def assertArrayEquals(self, a, b):
		'''Asserts that two arrays are equal'''
		self.assertTrue((a == b).all())

class DatabaseTest(BaseTest):
	'''A wrapper around BaseTest that tests for Database connections'''
	connection = None

	def test_connection(self):
		'''Tests the database connection'''
		self.assertHasAttr(self, "connection")
		self.assertEquals(self.connection.server_info()["ok"], 1.0)
