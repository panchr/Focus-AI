# Rushy Panchal
# tests/models/test_response.py

import unittest
import baseTests

from modelTestBase import CustomTypeTestBase
from models.response import Response

class TestResponse(CustomTypeTestBase, unittest.TestCase):
	'''Tests the models.response.Response Model'''
	model = Response
	mongoConversions = [
		([(), ()], [(), ()]), # no move
		([(2, 3), (1, 1)], [(2, 3), (1, 1)]), # simple move
		([(5, 2), [(5, 1), (2, 1)]], [(5, 2), [(5, 1), (2, 1)]]) # taking move
		]
