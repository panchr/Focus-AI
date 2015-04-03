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

	def test_hasIncreaseWeight(self):
		'''Has function increaseWeight'''
		self.assertFunctionExists(self.modelObject, "increaseWeight")

	def test_hasDecreaseWeight(self):
		'''Has function decreaseWeight'''
		self.assertFunctionExists(self.modelObject, "decreaseWeight")

	def test_hasNormalize(self):
		'''Has method normalize'''
		self.assertFunctionExists(self.model, "normalize")

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

	def test_normalize(self):
		'''Rule.normalize works'''
		numTests = 100
		newArray = lambda: np.zeros((8, 8), dtype = np.int32)

		rules = [models.Rule.new(newArray(), newArray(), [], initialWeight = random.randint(0, numTests)) for i in xrange(numTests)]

		sumWeight = float(sum(map(lambda rule: rule.weight, rules)))
		normalized = map(lambda rule: rule.weight / sumWeight, rules)
		
		models.Rule.normalize()

		for index, rule in enumerate(rules, 0):
			rule.reload()
			self.assertEquals(rule.weight, normalized[index])
			rule.delete()
