# Rushy Panchal
# ai/tests/core/test_errors.py

import unittest
import baseTests

from core.errors import WrongPlayerMove, InvalidMove

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
