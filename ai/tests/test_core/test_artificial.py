# Rushy Panchal
# ai/tests/core/test_artificial.py

import unittest
import baseTests
import numpy as np

from core.artificial import DynamicScriptingAI, BaseAI, StaticAI
from core.engine import Engine
from core.database import Database

import config
import models

def setup():
	'''Set up the test suite'''
	global conn
	conn = Database(host = config.DB_HOST, port = config.DB_PORT)
	db = conn[models.Model.__database__]
	models.Rule.__collection__ = baseTests.DatabaseTest.randomCollectionName(db)
	models.Game.__collection__ = baseTests.DatabaseTest.randomCollectionName(db)
	conn.register(models.Rule)
	conn.register(models.Game)
	models.register(conn)

	engine = Engine(database = conn)

	TestBaseAI.connection = conn
	TestBaseAI.engine = engine

def tearDown():
	'''Tear down the test suite'''
	conn[models.Rule.__database__].drop_collection(models.Rule.__collection__)

class TestBaseAI(baseTests.DatabaseTest, baseTests.NumpyTest, unittest.TestCase):
	'''Test the core.artificial.BaseAI class'''
	testClass = BaseAI

	@classmethod
	def setUpClass(cls):
		'''Sets up the class of testing'''	
		cls.game_id = cls.engine.newGame()	
		cls.testObject = cls.testClass(database = cls.connection, engine = cls.engine, game = cls.game_id, piece = 2)

	@classmethod
	def tearDownClass(cls):
		'''Cleanup the test class'''
		cls.connection.close()

	def test_makeMove(self):
		'''Raises proper error'''
		self.assertRaises(NotImplementedError, self.testObject.makeMove)

	def test_setState(self):
		'''BaseAI.setState works'''
		newState = "newState"

		self.assertNotEquals(self.testObject.state, newState)
		self.assertNotEquals(self.engine.games[self.game_id], newState)

		self.testObject.setState(newState)

		self.assertEquals(self.testObject.state, newState)
		self.assertEquals(self.engine.games[self.game_id], newState)

	def test_getAdjacent(self):
		'''StaticAI.getAdjacent works'''
		state = np.asarray([
			[0, 1, 0, 1, 0, 1, 0, 1],
			[1, 0, 1, 0, 1, 0, 1, 0],
			[0, 1, 0, 1, 0, 1, 0, 0],
			[0, 0, 2, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 1, 0, 0],
			[2, 0, 0, 0, 2, 0, 2, 0],
			[0, 2, 0, 2, 0, 2, 0, 2],
			[2, 0, 2, 0, 2, 0, 2, 0]
			], dtype = config.STORAGE_DATATYPE)
		self.testObject.setState(state)

		adjacent1 = sorted(self.testObject.getAdjacent((4, 4)))
		adjacent1_real = sorted([(3, 3), (3, 5), (5, 3), (5, 5)])
		adjacent2 = sorted(self.testObject.getAdjacent((6, 5)))
		adjacent2_real = sorted([(5, 4), (5, 6)])
		adjacent3 = sorted(self.testObject.getAdjacent((2, 3)))
		adjacent3_real = sorted([(3, 2), (3, 4)])

		partial_adjacent1 = sorted(self.testObject.getAdjacent((5, 0)))
		partial_adjacent1_real = sorted([(4, 1)])
		partial_adjacent2 = sorted(self.testObject.getAdjacent((0, 0)))
		partial_adjacent2_real = sorted([(1, 1)])
		partial_adjacent3 = sorted(self.testObject.getAdjacent((7, 4)))
		partial_adjacent3_real = sorted([(6, 3), (6, 5)])

		self.assertEquals(adjacent1, adjacent1_real)
		self.assertEquals(adjacent2, adjacent2_real)
		self.assertEquals(adjacent3, adjacent3_real)
		self.assertEquals(partial_adjacent1, partial_adjacent1_real)
		self.assertEquals(partial_adjacent2, partial_adjacent2_real)
		self.assertEquals(partial_adjacent3, partial_adjacent3_real)

	def test_getOpenings(self):
		'''StaticAI.getOpenings works'''
		state = np.asarray([
			[0, 1, 0, 1, 0, 1, 0, 1],
			[1, 0, 1, 0, 1, 0, 1, 0],
			[0, 1, 0, 1, 0, 1, 0, 0],
			[0, 0, 2, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 1, 0, 0],
			[2, 0, 0, 0, 2, 0, 2, 0],
			[0, 2, 0, 2, 0, 2, 0, 2],
			[2, 0, 2, 0, 2, 0, 2, 0]
			], dtype = config.STORAGE_DATATYPE)
		self.testObject.setState(state)

		openings = sorted(self.testObject.getOpenings((4, 5)))
		openings_real = sorted([])
		openings2 = sorted(self.testObject.getOpenings((2, 5)))
		openings2_real = sorted([(3, 4), (3, 6)])

		partial_openings = sorted(self.testObject.getOpenings((6, 7)))
		partial_openings_real = sorted([])
		partial_openings2 = sorted(self.testObject.getOpenings((5, 0)))
		partial_openings2_real = sorted([(4, 1)])

		self.assertEquals(openings, openings_real)
		self.assertEquals(openings2, openings2_real)
		self.assertEquals(partial_openings, partial_openings_real)
		self.assertEquals(partial_openings2, partial_openings2_real)

	def test_getOpponentOccupied(self):
		'''StaticAI.getOpponentOccupied works'''
		state = np.asarray([
			[0, 1, 0, 1, 0, 1, 0, 1],
			[1, 0, 1, 0, 1, 0, 1, 0],
			[0, 1, 0, 1, 0, 1, 0, 0],
			[0, 0, 2, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 1, 0, 0],
			[2, 0, 0, 0, 2, 0, 2, 0],
			[0, 2, 0, 2, 0, 2, 0, 2],
			[2, 0, 2, 0, 2, 0, 2, 0]
			], dtype = config.STORAGE_DATATYPE)
		self.testObject.setState(state)

		occupied = sorted(self.testObject.getOpponentOccupied((3, 2)))
		occupied_real = sorted([(2, 1), (2, 3)])

		occupied_partial = sorted(self.testObject.getOpponentOccupied((5, 0)))
		occupied_partial_real = []

		self.assertEquals(occupied, occupied_real)
		self.assertEquals(occupied_partial, occupied_partial_real)

class TestStaticAI(TestBaseAI):
	'''Tests the core.artificial.StaticAI class'''
	testClass = StaticAI

	def test_inheritsBaseAI(self):
		'''Inherits from BaseAI'''
		self.assertIsSubclass(self.testClass, BaseAI)
		self.assertIsSubclass(self.testClass, object)

	def test_instanceBaseAI(self):
		'''Instance of BaseAI'''
		self.assertIsInstance(self.testObject, BaseAI)
		self.assertIsInstance(self.testObject, object)

	def test_makeMove(self):
		'''StaticAI.makeMove works'''
		pass

class TestDynamicScriptingAI(TestStaticAI, TestBaseAI):
	'''Test the core.artificial.DynamicScriptingAI class'''
	testClass = DynamicScriptingAI

	@classmethod
	def setUpClass(cls):
		'''Set up the class for unit testing'''
		cls.game_id = cls.engine.newGame()

		cls.testObject = cls.testClass(database = cls.connection, engine = cls.engine, game = cls.game_id, piece = 2)

		cls.rulesAdded = []

		cls.stateC = np.asarray([
			[0, 1, 0, 1, 0, 1, 0, 1],
			[1, 0, 1, 0, 1, 0, 1, 0],
			[0, 1, 0, 1, 0, 1, 0, 0],
			[0, 0, 2, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 1, 0, 0],
			[2, 0, 0, 0, 2, 0, 2, 0],
			[0, 2, 0, 2, 0, 2, 0, 2],
			[2, 0, 2, 0, 2, 0, 2, 0]
			], dtype = config.STORAGE_DATATYPE)

		cls.rulesAdded.append(
			models.Rule.new(
			cls.stateC,
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 3, 0, 0, 0],
				[0, 0, 0, 0, 0, 1, 0, 0],
				[0, 0, 0, 0, 0, 0, 2, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = config.STORAGE_DATATYPE),
			[(5, 6), [(3, 4)]]
			))

		cls.stateD = np.asarray([
			[0, 1, 0, 1, 0, 1, 0, 1],
			[1, 0, 1, 0, 0, 0, 1, 0],
			[0, 1, 0, 1, 0, 1, 0, 1],
			[0, 0, 0, 0, 0, 0, 2, 0],
			[0, 1, 0, 2, 0, 0, 0, 0],
			[2, 0, 2, 0, 0, 0, 0, 0],
			[0, 2, 0, 2, 0, 2, 0, 2],
			[2, 0, 2, 0, 2, 0, 2, 0]
			], dtype = config.STORAGE_DATATYPE)

		modifiedStateD = np.copy(cls.stateD)
		modifiedStateD[-1, -1] = 2 # make this state less similar than the rest

		# For the complex rules only
		cls.rulesAdded.append(
			models.Rule.new(
			modifiedStateD,
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 1],
				[0, 0, 0, 0, 0, 0, 2, 0],
				[0, 0, 0, 0, 0, 3, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = config.STORAGE_DATATYPE),
			[(3, 6), (2, 5)]
			))

		cls.rulesAdded.append(
			models.Rule.new(
			modifiedStateD,
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 3, 0, 0, 0, 0, 0],
				[0, 1, 0, 0, 0, 0, 0, 0],
				[2, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = config.STORAGE_DATATYPE),
			[(5, 0), [(3, 2)]]
			))

		cls.rulesAdded.append(
			models.Rule.new(
			modifiedStateD,
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 3, 0, 0, 0],
				[0, 0, 0, 0, 0, 1, 0, 0],
				[0, 0, 0, 0, 0, 0, 2, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = config.STORAGE_DATATYPE),
			[(3, 6), [(1, 4)]]
			))

		cls.rulesAdded.append(
			models.Rule.new(
			cls.stateD,
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 3, 0, 0, 0],
				[0, 0, 0, 1, 0, 0, 0, 0],
				[0, 0, 3, 0, 0, 0, 0, 0],
				[0, 1, 0, 0, 0, 0, 0, 0],
				[2, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = config.STORAGE_DATATYPE),
			[(5, 0), [(3, 2), (1, 4)]],
			initialWeight = 2
			))

	@classmethod
	def tearDownClass(cls):
		'''Tear down the class after unit testing'''
		for rule in cls.rulesAdded:
			rule.delete()
		cls.connection.close()

	def setUp(self):
		'''Sets up the test case'''
		self.stimuli = [
			np.asarray([
				[0, 0, 0, 0, 0, 0, 3, 0],
				[0, 0, 0, 0, 0, 1, 0, 0],
				[0, 0, 0, 0, 3, 0, 0, 0],
				[0, 0, 0, 1, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = config.STORAGE_DATATYPE),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 3, 0, 0, 0, 0, 0, 0],
				[0, 0, 2, 0, 0, 0, 0, 0],
				[0, 0, 0, -1, 0, 0, 0, 0]
				], dtype = config.STORAGE_DATATYPE),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 3, 0, 0, 0, 0],
				[0, 0, 0, 0, 1, 0, 0, 0],
				[0, 0, 0, 0, 0, 2, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 2, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = config.STORAGE_DATATYPE),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 3, 0, 0, 0],
				[0, 0, 0, 0, 0, 1, 0, 0],
				[0, 0, 0, 0, 0, 0, 2, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = config.STORAGE_DATATYPE),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 1],
				[0, 0, 0, 0, 0, 0, 2, 0],
				[0, 0, 0, 0, 0, 3, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = config.STORAGE_DATATYPE),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 3, 0, 0, 0, 0, 0],
				[0, 1, 0, 0, 0, 0, 0, 0],
				[2, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = config.STORAGE_DATATYPE),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 3, 0, 0, 0],
				[0, 0, 0, 0, 0, 1, 0, 0],
				[0, 0, 0, 0, 0, 0, 2, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = config.STORAGE_DATATYPE),
			np.asarray([
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 3, 0, 0, 0],
				[0, 0, 0, 1, 0, 0, 0, 0],
				[0, 0, 3, 0, 0, 0, 0, 0],
				[0, 1, 0, 0, 0, 0, 0, 0],
				[2, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0]
				], dtype = config.STORAGE_DATATYPE)
			]
		self.testObject.possibleStimuli = self.stimuli
		self.stateA = np.asarray([
			[1, 1, 1, 1, 1, 1, 0, 1],
			[1, 1, 1, 1, 1, 1, 1, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 1, 0, 1, 0, 0],
			[0, 0, 2, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[2, 2, 0, 2, 2, 2, 2, 2],
			[2, 2, 2, 2, 2, 2, 2, 2],
			], dtype = config.STORAGE_DATATYPE)
		self.stateB = np.asarray([
			[1, 1, 1, 1, 1, 1, 0, 1],
			[1, 1, 1, 1, 1, 1, 1, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 1, 0, 1, 0, 0],
			[0, 0, 2, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[2, 2, 2, 0, 2, 2, 2, 2],
			[2, 2, 2, -1, 2, 2, 2, 2],
			], dtype = config.STORAGE_DATATYPE)

	def test_inheritsStaticAI(self):
		'''DynamicScriptingAI inherits from StaticAI'''
		self.assertIsSubclass(self.testClass, StaticAI)

	def test_instanceStaticAI(self):
		'''Instance of StaticAI'''
		self.assertIsInstance(self.testObject, StaticAI)

	def test_makeMove(self):
		'''DynamicScriptingAI.makeMove works'''
		self.testObject.setState(self.stateC)
		copyC = np.copy(self.stateC)

		# Make sure they are equal to start with
		self.assertEquals(self.testObject.state, copyC)

		self.testObject.makeMove()
		copyC[5, 6] = 0
		copyC[4, 5] = 0
		copyC[3, 4] = 2

		self.assertEquals(self.testObject.state, copyC)

	def test_makeMoveComplex(self):
		'''DynamicScriptingAI.makeMove works (with more complicated moves'''
		self.engine.gameMeta[self.game_id]["move"] = 2
		self.testObject.setState(self.stateD)
		copyD = np.copy(self.stateD)

		# Make sure the states are equal to start with
		self.assertEquals(self.testObject.state, copyD)

		self.testObject.makeMove()
		copyD[5, 0] = 0
		copyD[4, 1] = 0
		copyD[2, 3] = 0
		copyD[1, 4] = 2

		self.assertEquals(self.testObject.state, copyD)

	def test_analyzeStimuli(self):
		'''DynamicScriptingAI.analyzeStimuli works'''
		self.testObject.setState(self.stateA)
		stimuli = self.testObject.analyzeStimuli()
		self.assertEquals(stimuli, self.stimuli[:1])

		self.testObject.setState(self.stateB)
		stimuli = self.testObject.analyzeStimuli()
		self.assertEquals(stimuli, self.stimuli[:2])

	def test_feedback(self):
		'''DynamicScriptingAI.feedback works'''
		self.testObject.playedMoves = self.rulesAdded
		self.testObject.history = [np.ndarray((8, 8), dtype = config.STORAGE_DATATYPE) for i in xrange(10)]
		initialCount = self.connection.Game.find().count()

		self.testObject.feedback(True, "It sure fooled me!")

		feedback = self.connection.Game.find_one()
		if not feedback:
			self.fail("Feedback not inserted into database")

		self.assertEquals(self.connection.Game.find().count(), initialCount + 1)
		self.assertEquals(feedback.feedback, "It sure fooled me!")
		self.assertEquals(feedback.seemedHuman, True)
		self.assertEquals(len(feedback.history), len(self.testObject.history))
		for x in feedback.history:
			self.assertInArray(x, self.testObject.history)
		self.assertEquals(sorted(feedback.rules), sorted(map(lambda move: move._id, self.rulesAdded)))
