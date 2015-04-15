# Rushy Panchal
# ai/tests/core/test_errors.py

import unittest
import baseTests

from core.errors import *

class ErrorTest(unittest.TestCase, baseTests.BaseTest):
	'''Test the core.errors Error classes'''
	errorClasses = [WrongPlayerMove, InvalidMove]

	def test_areErrors(self):
		'''Each error is a subclass of the Exception class'''
		for error in self.errorClasses:
			self.assertIsSubclass(error, Exception)
			self.assertIsInstance(error(), Exception)

	def test_raiseErrors(self):
		'''Each error can be raised'''
		def raiseError(error):
			'''Helper method to raise an error'''
			raise error("Test Message")

		for error in self.errorClasses:
			self.assertRaises(error, raiseError, error)

class BaseErrorTest(baseTests.BaseTest):
	'''Base class for testing the errors'''
	error = Exception # override in each test class
	errorCode = 500
	errorMessage = "Something went wrong"

	def setUp(self):
		'''Set up should not be run for these classes'''
		pass

	def test_isException(self):
		'''error is a subclass of the Exception class'''
		self.assertIsSubclass(self.error, Exception)

	def test_hasCode(self):
		'''error.errorCode attribute exists'''
		self.assertHasAttr(self.error, "errorCode")
		self.assertIsInstance(self.error.errorCode, int)

	def test_code(self):
		'''error.errorCode is the proper code'''
		self.assertEquals(self.error.errorCode, self.errorCode)

	def test_hasMessage(self):
		'''error.errorMessage exists'''
		self.assertHasAttr(self.error, "errorMessage")
		self.assertIsInstance(self.error.errorMessage, str)

	def test_message(self):
		'''error.errorMessage is the proper message'''
		self.assertEquals(self.error.errorMessage, self.errorMessage)

	def test_raises(self):
		'''error can be raised'''
		def raiseError():
			raise self.error()
		self.assertRaises(self.error, raiseError)

class SubErrorTest(BaseErrorTest):
	'''Child-base class for testing the errors'''
	def test_isBaseError(self):
		'''error is a subclass of the BaseError class'''
		self.assertIsSubclass(self.error, BaseError)

class TestBaseError(BaseErrorTest, unittest.TestCase):
	'''Test the controllers.error.BaseError class'''
	error = BaseError
	errorCode = 500
	errorMessage = "Something went wrong"

class TestMalformedQuery(SubErrorTest, unittest.TestCase):
	'''Tests the controllers.error.MalformedQuery class'''
	error = MalformedQuery
	errorCode = 400
	errorMessage = "Bad request"

class TestNotFound(SubErrorTest, unittest.TestCase):
	'''Tests the controllers.error.NotFound class'''
	error = NotFound
	errorCode = 404
	errorMessage = "Not found"
