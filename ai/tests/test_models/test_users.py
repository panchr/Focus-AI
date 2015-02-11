# Rushy Panchal
# tests/models/test_users.py

import unittest
import baseTests

from modelTestBase import ModelTestBase
from models.user import User

class TestUser(unittest.TestCase, ModelTestBase):
	'''Tests the models.users.User Model'''
	def setUp(self):
		'''Set up the test case'''
		self.model = User
		self.modelObject = self.model()
