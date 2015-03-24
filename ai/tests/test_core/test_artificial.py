# Rushy Panchal
# ai/tests/core/test_artificial.py

import unittest
import baseTests

from core.artificial import DynamicScriptingAI

class TestDynamicScriptingAI(unittest.TestCase, baseTests.BaseTest):
	'''Test the core.artificial.DynamicScriptingAI class'''
	testClass = DynamicScriptingAI

	def setUp(self):
		'''Sets up the test case'''
		self.testObject = self.testClass()

	def test_hasMakeMove(self):
		'''DynamicScriptingAI.makeMove method exists'''
		self.assertFunctionExists(self.testClass, "makeMove")

	def test_hasAnalyzeStimuli(self):
		'''DynamicScriptingAI.analyzeStimuli method exists'''
		self.assertFunctionExists(self.testClass, "analyzeStimuli")

	def test_makeMove(self):
		'''DynamicScriptingAI.makeMove works'''
		pass # not implemented yet

	def test_analyzeStimuli(self):
		'''DynamicScriptingAI.analyzeStimuli works'''
		pass # not implemented yet
