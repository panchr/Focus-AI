# Rushy Panchal
# ai/tests/core/test_database.py

import unittest
import baseTests

from core.database import Database

class TestDatabase(unittest.TestCase, baseTests.BaseTest, object):
	'''Test the core.database.Database class'''
	testClass = Database

	def tearDown(self):
		'''Tears down the test cases'''
		# make sure to end the connection
		pass

	def test_hasGetMatchingRules(self):
		'''Database has getMatchingRules method'''
		self.assertFunctionExists(self.testClass, "getMatchingRules")

	def test_hasGetStimuli(self):
		'''Database has getStimuli method'''
		self.assertFunctionExists(self.testClass, "getStimuli") 

	def test_getMatchingRules(self):
		'''Database.getMatchingRules works'''
		pass # not implemented yet

	def test_getStimuli(self):
		'''Database.getStimuli works'''
		pass # not implemented yet
