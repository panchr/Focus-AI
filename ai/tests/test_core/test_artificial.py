# Rushy Panchal
# ai/tests/core/test_artificial.py

import unittest
import baseTests
import numpy as np

from core.artificial import DynamicScriptingAI

class TestDynamicScriptingAI(baseTests.NumpyTest, unittest.TestCase):
	'''Test the core.artificial.DynamicScriptingAI class'''
	testClass = DynamicScriptingAI

	def setUp(self):
		'''Sets up the test case'''
		self.testObject = self.testClass()
		self.stimuli = [
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 1, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 1, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				], dtype = np.int32),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, -1, 0, 0, 0, 0],
				], dtype = np.int32),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 1, 0, 0, 0],
				[0, 0, 0, 0, 0, 2, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 2, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				], dtype = np.int32)
			]
		self.testObject.possibleStimuli = self.stimuli
		self.stateA = np.asarray([
			[1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 1, 0, 1, 0, 0],
			[0, 0, 2, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[2, 2, 0, 2, 2, 2, 2, 2],
			[2, 2, 2, 2, 2, 2, 2, 2],
			], dtype = np.int32)
		self.stateB = np.asarray([
			[1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 1, 0, 1, 0, 0],
			[0, 0, 2, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[2, 2, 2, 0, 2, 2, 2, 2],
			[2, 2, 2, -1, 2, 2, 2, 2],
			], dtype = np.int32)

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
		self.testObject.state = self.stateA
		stimuli = self.testObject.analyzeStimuli()
		self.assertEquals(stimuli, self.stimuli[:1])

		self.testObject.state = self.stateB
		stimuli = self.testObject.analyzeStimuli()
		self.assertEquals(stimuli, self.stimuli[:2])
