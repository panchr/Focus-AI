# Rushy Panchal
# ai/tests/core/test_database.py

import unittest
import baseTests

from core.database import Database

import models
import numpy as np

from models.state import Gamestate

def setup():
	'''Setup the test suite'''
	global conn
	conn = Database(host = baseTests.TEST_HOST, port = baseTests.TEST_PORT)
	models.Rule.__collection__ = baseTests.DatabaseTest.randomCollectionName(conn[models.Rule.__database__])
	conn.register(models.Rule)
	models.register(conn)
	TestDatabase.connection = conn

def tearDown():
	'''Tear down the test suite'''
	conn[models.Rule.__database__].drop_collection(models.Rule.__collection__)

class TestDatabase(baseTests.DatabaseTest, baseTests.NumpyTest, unittest.TestCase):
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
				], dtype = np.int32),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, -1, 0, 0, 0, 0],
				], dtype = np.int32),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 1, 0, 0, 0],
				[0, 0, 0, 0, 0, 2, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 2, 0, 0, 0, 0],
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
		toMatch = [
			[np.asarray([
				[1, 1, 1, 1, 1, 1, 1, 1],
				[1, 1, 1, 1, 1, 0, 1, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 1, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 1, 0, 0, 0, 0],
				[2, 2, 2, 2, 2, 2, 2, 2],
				[2, 2, 2, 2, 2, 2, 2, 2],
				], dtype = np.int32),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 1, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 1, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				], dtype = np.int32)]
			]

		for board_stimuli, rule in zip(toMatch, self.rules):
			board, stimuli = board_stimuli
			matched = self.connection.getMatchingRules(board, [stimuli])
			for key, value in rule.items():
				self.assertEquals(value, matched[0][key])

	def test_getStimuli(self):
		'''Database.getStimuli works'''
		stimuliToTest = self.connection.getStimuli()
		rawStimuli = self.conditions
		for stimulus in rawStimuli:
			self.assertInArray(stimulus, stimuliToTest)
		self.assertEquals(len(stimuliToTest), len(rawStimuli))
