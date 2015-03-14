# Rushy Panchal
# ai/tests/core/test_database.py

import unittest
import baseTests

from core.database import Database

import models
import numpy as np

def setup():
	'''Setup the test suite'''
	conn = Database(host = baseTests.TEST_HOST, port = baseTests.TEST_PORT)
	conn.register(models.Rule)
	models.register(conn)
	TestDatabase.connection = conn

class TestDatabase(unittest.TestCase, baseTests.DatabaseTest, baseTests.NumpyTest, object):
	'''Test the core.database.Database class'''
	testClass = Database

	@classmethod
	def setUpClass(cls):
		'''Set up the class'''
		conditions = [
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 1, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 1, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				], dtype = np.int32)
			]
		rules = []
		for condition in conditions:
			rule = models.Rule.new(np.ndarray((8, 8), dtype = np.int32), condition, [])
			rules.append(rule)
		cls.rules = rules
		cls.conditions = conditions

	@classmethod
	def tearDownClass(cls):
		'''Tear down the class'''
		for rule in cls.rules:
			rule.delete()

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
		dbStimuli = self.connection.getStimuli()
		stimuliToTest = map(lambda rule: rule.condition, dbStimuli)
		rawStimuli = self.conditions
		for stimulus in rawStimuli:
			self.assertInArray(stimulus, stimuliToTest)
		self.assertEquals(len(stimuliToTest), len(rawStimuli))
