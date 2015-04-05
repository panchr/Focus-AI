# Rushy Panchal
# ai/tests/core/test_database.py

import unittest
import baseTests

import numpy as np
import models

import config
from models.state import Gamestate
from core.database import Database

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
				], dtype = config.STORAGE_DATATYPE),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, -1, 0, 0, 0, 0],
				], dtype = config.STORAGE_DATATYPE),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 1, 0, 0, 0],
				[0, 0, 0, 0, 0, 2, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 2, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				], dtype = config.STORAGE_DATATYPE)
			]
		rules = []
		for condition in conditions:
			rule = models.Rule.new(np.ndarray((8, 8), dtype = config.STORAGE_DATATYPE), condition, [])
			rules.append(rule)
		cls.rules = rules
		cls.conditions = conditions

	@classmethod
	def tearDownClass(cls):
		'''Tear down the class'''
		for rule in cls.rules:
			rule.delete()

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
				], dtype = config.STORAGE_DATATYPE),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 1, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 1, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				], dtype = config.STORAGE_DATATYPE)]
			]

		for board_stimuli, rule in zip(toMatch, self.rules):
			board, stimuli = board_stimuli
			matched = self.connection.getMatchingRules(board, [stimuli], 2)
			for key, value in rule.items():
				self.assertEquals(value, matched[0][key])

	def test_getStimuli(self):
		'''Database.getStimuli works'''
		stimuliToTest = self.connection.getStimuli()
		rawStimuli = self.conditions
		for stimulus in rawStimuli:
			self.assertInArray(stimulus, stimuliToTest)
		self.assertEquals(len(stimuliToTest), len(rawStimuli))

	def test_newRule(self):
		'''Database.newRule works'''
		current_rules = map(lambda rule: rule.condition, list(self.connection.Rule.find({}, {"condition": 1})))

		state = np.random.random_integers(-2, 2, (8, 8))
		condition = np.random.random_integers(-2, 2, (8, 8))
		response = [(5, 5), (2, 3)] # random response, not actually valid

		while self.inArray(condition, current_rules):
			condition = np.random.random_integers(-2, 2, (8, 8))

		rule = self.connection.newRule(state, condition, response)
		self.rules.append(rule)
		converter = Gamestate()
		newRule = self.connection.Rule.find_one({"state": converter.to_bson(state), "condition": converter.to_bson(condition)})

		self.assertNotEquals(newRule, None) # if newRule is None, then the find was not successful
