# Rushy Panchal
# tests/models/test_bitstring.py

import unittest
import baseTests

from modelTestBase import CustomTypeTestBase
from models.bitstring import Bitstring
from models.integer import Integer, Long

class TestBitstring(CustomTypeTestBase, unittest.TestCase):
	'''Tests the models.bitstring.Bitstring Model'''
	model = Bitstring
	mongoConversions = [
		(25L, Long(25)),
		(15L, Long(15)),
		(2**64 - 1, Long(2**64 - 1))
		]
