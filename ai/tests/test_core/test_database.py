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
