# Rushy Panchal
# ai/tests/core/test_database.py

import unittest
import baseTests

from core.database import Database

class TestDatabase(unittest.TestCase, baseTests.BaseTest, object):
	'''Test the core.database.Database class'''
	def setUp(self):
		'''Sets up the test cases'''
		self.testClass = Database

	def tearDown(self):
		'''Tears down the test cases'''
		# make sure to end the connection
		pass

	def test_hasGetMatchingRules(self):
		'''has getMatchingRules method'''
		self.assertFunctionExists(self.testClass, "getMatchingRules")
