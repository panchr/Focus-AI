# Rushy Panchal
# tests/models/test_condition.py

import unittest
import baseTests

from modelTestBase import CustomTypeTestBase
from test_state import TestGamestate

from models.condition import Condition

class TestCondition(TestGamestate):
	'''Tests the models.condition.Condition Model'''
	model = Condition
