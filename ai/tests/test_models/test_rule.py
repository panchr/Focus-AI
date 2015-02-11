# Rushy Panchal
# tests/models/test_rule.py

import unittest
import baseTests

from modelTestBase import ModelTestBase
from models.rule import Rule

class TestRule(unittest.TestCase, ModelTestBase):
	'''Tests the models.rule.Rule Model'''
	def setUp(self):
		'''Set up the test case'''
		self.model = Rule
		self.modelObject = self.model()

	def test_hasIncreaseWeight(self):
		'''Has function increaseWeight'''
		self.assertFunctionExists(self.modelObject, "increaseWeight")

	def test_hasDecreaseWeight(self):
		'''Has function decreaseWeight'''
		self.assertFunctionExists(self.modelObject, "decreaseWeight")

	def test_increaseWeight(self):
		'''increaseWeight works'''
		currentWeight = self.modelObject.weight
		self.modelObject.increaseWeight(save = False)
		self.assertEquals(self.modelObject.weight, currentWeight + 1)
		
	def test_decreaseWeight(self):
		'''decreaseWeight works'''
		currentWeight = self.modelObject.weight
		self.modelObject.decreaseWeight(save = False)
		self.assertEquals(self.modelObject.weight, currentWeight - 1)
