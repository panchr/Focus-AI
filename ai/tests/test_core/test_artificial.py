# Rushy Panchal
# ai/tests/core/test_artificial.py

import unittest
import baseTests
import numpy as np

from core.artificial import DynamicScriptingAI
from core.engine import Engine
from core.database import Database

import config
import models

class TestDynamicScriptingAI(baseTests.NumpyTest, unittest.TestCase):
	'''Test the core.artificial.DynamicScriptingAI class'''
	testClass = DynamicScriptingAI

	@classmethod
	def setUpClass(cls):
		'''Set up the class for unit testing'''
		cls.db = Database(host = config.HOST, port = config.PORT)
		cls.db.register(models.Rule)
		models.register(cls.db)
		
		# models.Rule(np.asarray([
		# 	[0, 1, 0, 1, 0, 1, 0, 1],
		# 	[1, 0, 1, 0, 1, 0, 1, 0],
		# 	[0, 1, 0, 1, 0, 1, 0, 0],
		# 	[0, 0, 2, 0, 0, 0, 0, 0],
		# 	[0, 0, 0, 0, 0, 1, 0, 0],
		# 	[2, 0, 0, 0, 2, 0, 2, 0],
		# 	[0, 2, 0, 2, 0, 2, 0, 2],
		# 	[2, 0, 2, 0, 2, 0, 2, 0]
		# 	], dtype = np.int32), np.asarray([
		# 		[0, 0, 0, 0, 0, 0, 0, 0],
		# 		[0, 0, 0, 0, 0, 0, 0, 0],
		# 		[0, 0, 0, 0, 0, 0, 0, 0],
		# 		[0, 0, 0, 0, 0, 0, 0, 0],
		# 		[0, 0, 0, 0, 0, 1, 0, 0],
		# 		[0, 0, 0, 0, 0, 0, 2, 0],
		# 		[0, 0, 0, 0, 0, 0, 0, 0],
		# 		[0, 0, 0, 0, 0, 0, 0, 0]
		# 		], dtype = np.int32), [(5, 6), (3, 4)])

		cls.engine = Engine(database = cls.db)
		game_id = cls.engine.newGame()

		cls.testObject = cls.testClass(database = cls.db, engine = cls.engine, game = game_id)

	@classmethod
	def tearDownClass(cls):
		'''Tear down the class after unit testing'''
		cls.db.close()

	def setUp(self):
		'''Sets up the test case'''
		self.stimuli = [
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 1, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 1, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = np.int32),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, -1, 0, 0, 0, 0]
				], dtype = np.int32),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 1, 0, 0, 0],
				[0, 0, 0, 0, 0, 2, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 2, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = np.int32),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 1, 0, 0],
				[0, 0, 0, 0, 0, 0, 2, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
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
		self.stateC = np.asarray([
			[0, 1, 0, 1, 0, 1, 0, 1],
			[1, 0, 1, 0, 1, 0, 1, 0],
			[0, 1, 0, 1, 0, 1, 0, 0],
			[0, 0, 2, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 1, 0, 0],
			[2, 0, 0, 0, 2, 0, 2, 0],
			[0, 2, 0, 2, 0, 2, 0, 2],
			[2, 0, 2, 0, 2, 0, 2, 0]
			], dtype = np.int32)

	def test_hasMakeMove(self):
		'''DynamicScriptingAI.makeMove method exists'''
		self.assertFunctionExists(self.testObject, "makeMove")

	def test_hasAnalyzeStimuli(self):
		'''DynamicScriptingAI.analyzeStimuli method exists'''
		self.assertFunctionExists(self.testObject, "analyzeStimuli")

	def test_makeMove(self):
		'''DynamicScriptingAI.makeMove works'''
		self.testObject.state = self.stateC

		# need to make sure it is performing moves that actually contains the given stimuli
		# also need to consider when there are no stimuli found - random move?
		pass # not implemented yet

	def test_analyzeStimuli(self):
		'''DynamicScriptingAI.analyzeStimuli works'''
		self.testObject.state = self.stateA
		stimuli = self.testObject.analyzeStimuli()
		self.assertEquals(stimuli, self.stimuli[:1])

		self.testObject.state = self.stateB
		stimuli = self.testObject.analyzeStimuli()
		self.assertEquals(stimuli, self.stimuli[:2])
