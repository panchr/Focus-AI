# Rushy Panchal
# tests/controllers/test_response.py

import unittest
import baseTests

import json
import arrow

from core.response import Response

class TestResponse(baseTests.BaseTest, unittest.TestCase):
	'''Test the controllers.response.Response Controller'''
	controllerBase = Response

	def setUp(self):
		'''Sets up the test case'''
		self.controller = Response

	def test_hasError(self):
		'''has function error'''
		self.assertFunctionExists(self.controller, "error")

	def test_hasJson(self):
		'''has function json'''
		self.assertFunctionExists(self.controller, "json")

	def test_jsonTime(self):
		'''function json raw timestamp works'''
		testRaw = json.dumps(self.controller.json("Test Message", "Success", 200))
		testJson = json.loads(testRaw)
		testDict = {
			"message": "Test Message",
			"status": "Success",
			"type": 200,
			"timestamp": testJson["timestamp"]
			}
		self.assertEquals(testJson, testDict)
		self.assertEquals(testRaw, json.dumps(testDict))

	def test_jsonStatusCode(self):
		'''function json no status code works'''
		testRaw = json.dumps(self.controller.json("Test Message", "Success", timestamp = "Now"))
		testJson = json.loads(testRaw)
		testDict = {
			"message": "Test Message",
			"status": "Success",
			"type": 200,
			"timestamp": "Now",
			}
		self.assertEquals(testJson, testDict)

	def test_jsonStatusCodeInt(self):
		'''function json no status code with status as int works'''
		testRaw = json.dumps(self.controller.json("Test Message", 400, timestamp = "Now"))
		testJson = json.loads(testRaw)
		testDict = {
			"message": "Test Message",
			"status": 400,
			"type": 400,
			"timestamp": "Now",
			}
		self.assertEquals(testJson, testDict)

	def test_jsonData(self):
		'''function json with data parameters works'''
		testRaw = json.dumps(self.controller.json("Test Message", "Not Found", 404, "Now", user = "panchr", value = 25))
		testJson = json.loads(testRaw)
		testDict = {
			"message": "Test Message",
			"status": "Not Found",
			"type": 404,
			"timestamp": "Now",
			"user": "panchr",
			"value": 25
			}
		self.assertEquals(testJson, testDict)
