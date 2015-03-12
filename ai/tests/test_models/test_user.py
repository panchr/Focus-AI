# Rushy Panchal
# tests/models/test_user.py

import unittest
import baseTests

from modelTestBase import ModelTestBase
from models.user import User

class TestUser(ModelTestBase, unittest.TestCase):
	'''Tests the models.users.User Model'''
	model = User
