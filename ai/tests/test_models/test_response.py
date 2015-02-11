# Rushy Panchal
# tests/models/test_response.py

import unittest
import baseTests

from modelTestBase import CustomTypeTestBase
from models.response import Response

class TestResponse(unittest.TestCase, CustomTypeTestBase):
	'''Tests the models.response.Response Model'''
	def setUp(self):
		'''Set up the test case'''
		self.model =  Response
		self.modelObject = self.model()

		self.mongoConversions = [
			("response", "response"),
			("good-response", "good-response")
			]
