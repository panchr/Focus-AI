# Rushy Panchal
# tests/models/test_bitstring.py

import unittest
import baseTests

from modelTestBase import CustomTypeTestBase
from models.bitstring import Bitstring
from models.integer import Integer, Long

class TestBitstring(unittest.TestCase, CustomTypeTestBase):
	'''Tests the models.bitstring.Bitstring Model'''
	def setUp(self):
		'''Set up the test case'''
		self.model = Bitstring
		self.modelObject = self.model()
		self.mongoConversions = [
			(25L, Long(25)),
			(15L, Long(15)),
			(2**64 - 1, Long(2**64 - 1))
			]
