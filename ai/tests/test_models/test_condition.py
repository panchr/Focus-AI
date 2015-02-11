# Rushy Panchal
# tests/models/test_condition.py

import unittest
import baseTests

from modelTestBase import CustomTypeTestBase
from models.condition import Condition

class TestCondition(unittest.TestCase, CustomTypeTestBase):
	'''Tests the models.condition.Condition Model'''
	def setUp(self):
		'''Set up the test case'''
		self.model =  Condition
		self.modelObject = self.model()

		self.mongoConversions = [
			("condition", "condition"),
			("bad-condition", "bad-condition")
			]
