# Rushy Panchal
# tests/models/test_rule.py

import unittest
import baseTests
from modelTestBase import ModelTestBase

import random
import mongokit
import numpy as np

import models
import config

def setup():
	'''Setup the test suite'''
	global conn
	conn = mongokit.Connection(host = baseTests.TEST_HOST, port = baseTests.TEST_PORT)
	models.Rule.__collection__ = baseTests.DatabaseTest.randomCollectionName(conn[models.Rule.__database__])
	conn.register(models.Rule)
	models.register(conn)
	TestRule.connection = conn

def tearDown():
	'''Tear down the test suite'''
	conn[models.Rule.__database__].drop_collection(models.Rule.__collection__)

class TestRule(baseTests.DatabaseTest, ModelTestBase, unittest.TestCase):
	'''Tests the models.rule.Rule Model'''
	model = models.Rule

	@classmethod
	def setUpClass(cls):
		'''Sets up the class of test cases'''
		cls.modelObject = cls.model()

		cls.groupName = "test_group"
		cls.getWeights = lambda self, rules: map(lambda item: item.weight, rules)
		cls.getStrengths = lambda self, rules: map(lambda item: item.strength, rules)
		cls.reloadRules = lambda self, rules: map(lambda item: item.reload(), rules)
		cls.deleteRules = lambda self, rules: map(lambda item: item.delete(), rules)	

	def test_deltaField(self):
		'''deltaField works'''
		currentWeight = self.modelObject.weight
		self.modelObject.deltaField(field = "weight", delta = config.WEIGHT_DELTA)
		self.assertEquals(self.modelObject.weight, currentWeight + config.WEIGHT_DELTA)

		currentWeight = self.modelObject.weight
		self.modelObject.deltaField(field = "weight", delta = -1 * config.WEIGHT_DELTA)
		self.assertEquals(self.modelObject.weight, currentWeight - config.WEIGHT_DELTA)

	def test_increaseWeight(self):
		'''increaseWeight works'''
		currentWeight = self.modelObject.weight
		self.modelObject.increaseWeight(save = False)
		self.assertEquals(self.modelObject.weight, currentWeight + config.WEIGHT_DELTA)

	def test_decreaseWeight(self):
		'''decreaseWeight works'''
		currentWeight = self.modelObject.weight
		self.modelObject.decreaseWeight(save = False)
		self.assertEquals(self.modelObject.weight, currentWeight - config.WEIGHT_DELTA)

	def test_increaseStrength(self):
		'''increaseStrength works'''
		currentStrength = self.modelObject.strength
		self.modelObject.increaseStrength(save = False)
		self.assertEquals(self.modelObject.strength, currentStrength + config.WEIGHT_DELTA)

	def test_decreaseStrength(self):
		'''decreaseStrength works'''
		currentStrength = self.modelObject.strength
		self.modelObject.decreaseStrength(save = False)
		self.assertEquals(self.modelObject.strength, currentStrength - config.WEIGHT_DELTA)

	def test_increaseWeightGroup(self):
		'''increaseWeight works for groups'''
		state = np.zeros((8, 8), dtype = np.int32)
		self.baseRule = self.model.new(state, state, [], group = self.groupName)
		self.testRules = [self.model.new(state, state, [], group = self.groupName) for i in xrange(5)]
		self.testRules_groupB = [self.model.new(state, state, [], group = self.groupName + "_b") for i in xrange(5)]

		initialWeights = self.getWeights(self.testRules)
		initialWeightsB = self.getWeights(self.testRules_groupB)
		initialBaseWeight = self.baseRule.weight

		self.baseRule.increaseWeight()

		self.baseRule.reload()
		self.reloadRules(self.testRules)
		self.reloadRules(self.testRules_groupB)

		newWeights = self.getWeights(self.testRules)	
		newWeightsB = self.getWeights(self.testRules_groupB)

		self.assertEquals(newWeights, map(lambda x: x + config.WEIGHT_DELTA, initialWeights))
		self.assertEquals(newWeightsB, initialWeightsB)
		self.assertEquals(self.baseRule.weight, initialBaseWeight + config.WEIGHT_DELTA)

		self.deleteRules(self.testRules + self.testRules_groupB + [self.baseRule])

	def test_decreaseWeightGroup(self):
		'''decreaseWeight works for groups'''
		state = np.zeros((8, 8), dtype = np.int32)
		self.baseRule = self.model.new(state, state, [], group = self.groupName)
		self.testRules = [self.model.new(state, state, [], group = self.groupName) for i in xrange(5)]
		self.testRules_groupB = [self.model.new(state, state, [], group = self.groupName + "_b") for i in xrange(5)]

		initialWeights = self.getWeights(self.testRules)
		initialWeightsB = self.getWeights(self.testRules_groupB)
		initialBaseWeight = self.baseRule.weight

		self.baseRule.decreaseWeight()

		self.baseRule.reload()
		self.reloadRules(self.testRules)
		self.reloadRules(self.testRules_groupB)

		newWeights = self.getWeights(self.testRules)	
		newWeightsB = self.getWeights(self.testRules_groupB)

		self.assertEquals(newWeights, map(lambda x: x - config.WEIGHT_DELTA, initialWeights))
		self.assertEquals(newWeightsB, initialWeightsB)
		self.assertEquals(self.baseRule.weight, initialBaseWeight - config.WEIGHT_DELTA)

		self.deleteRules(self.testRules + self.testRules_groupB + [self.baseRule])

	def test_increaseStrengthGroup(self):
		'''increaseStrength works for groups'''
		state = np.zeros((8, 8), dtype = np.int32)
		self.baseRule = self.model.new(state, state, [], group = self.groupName)
		self.testRules = [self.model.new(state, state, [], group = self.groupName) for i in xrange(5)]
		self.testRules_groupB = [self.model.new(state, state, [], group = self.groupName + "_b") for i in xrange(5)]

		initialStrengths = self.getStrengths(self.testRules)
		initialStrengthsB = self.getStrengths(self.testRules_groupB)
		initialBaseStrength = self.baseRule.strength

		self.baseRule.increaseStrength()

		self.baseRule.reload()
		self.reloadRules(self.testRules)
		self.reloadRules(self.testRules_groupB)

		newStrengths = self.getStrengths(self.testRules)	
		newStrengthsB = self.getStrengths(self.testRules_groupB)

		self.assertEquals(newStrengths, map(lambda x: x + config.WEIGHT_DELTA, initialStrengths))
		self.assertEquals(newStrengthsB, initialStrengthsB)
		self.assertEquals(self.baseRule.strength, initialBaseStrength + config.WEIGHT_DELTA)

		self.deleteRules(self.testRules + self.testRules_groupB + [self.baseRule])

	def test_decreaseStrengthGroup(self):
		'''decreaseStrength works for groups'''
		state = np.zeros((8, 8), dtype = np.int32)
		self.baseRule = self.model.new(state, state, [], group = self.groupName)
		self.testRules = [self.model.new(state, state, [], group = self.groupName) for i in xrange(5)]
		self.testRules_groupB = [self.model.new(state, state, [], group = self.groupName + "_b") for i in xrange(5)]

		initialStrengths = self.getStrengths(self.testRules)
		initialStrengthsB = self.getStrengths(self.testRules_groupB)
		initialBaseStrength = self.baseRule.strength

		self.baseRule.decreaseStrength()

		self.baseRule.reload()
		self.reloadRules(self.testRules)
		self.reloadRules(self.testRules_groupB)

		newStrengths = self.getStrengths(self.testRules)	
		newStrengthsB = self.getStrengths(self.testRules_groupB)

		self.assertEquals(newStrengths, map(lambda x: x - config.WEIGHT_DELTA, initialStrengths))
		self.assertEquals(newStrengthsB, initialStrengthsB)
		self.assertEquals(self.baseRule.strength, initialBaseStrength - config.WEIGHT_DELTA)

		self.deleteRules(self.testRules + self.testRules_groupB + [self.baseRule])

	def test_normalize(self):
		'''Rule.normalize works'''
		numTests = 100
		newArray = lambda: np.zeros((8, 8), dtype = config.STORAGE_DATATYPE)

		self.deleteRules(self.connection.Rule.find()) # clear any previous rules
		rules = [models.Rule.new(newArray(), newArray(), [], initialWeight = random.randint(0, numTests)) for i in xrange(numTests)]

		sumWeight = float(sum(map(lambda rule: rule.weight, rules))) or 1
		sumStrength = float(sum(map(lambda rule: rule.strength, rules))) or 1
		normalizedWeights = map(lambda rule: rule.weight / sumWeight, rules)
		normalizedStrengths = map(lambda rule: rule.strength / sumStrength, rules)
		
		models.Rule.normalize()

		for index, rule in enumerate(rules, 0):
			rule.reload()
			self.assertEquals(rule.weight, normalizedWeights[index])
			self.assertEquals(rule.strength, normalizedStrengths[index])
			rule.delete()
