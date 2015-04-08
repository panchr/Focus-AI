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

class TestStaticAI(TestBaseAI):
	'''Tests the core.artificial.StaticAI class'''
	testClass = StaticAI

	@classmethod
	def tearDownClass(cls):
		'''Tears down the class'''
		cls.connection.close()

	def test_inheritsBaseAI(self):
		'''Inherits from BaseAI'''
		self.assertIsSubclass(self.testClass, BaseAI)
		self.assertIsSubclass(self.testClass, object)

	def test_instanceBaseAI(self):
		'''Instance of BaseAI'''
		self.assertIsInstance(self.testObject, BaseAI)
		self.assertIsInstance(self.testObject, object)

	def test_evaluateAttack(self):
		'''StaticAI.evaluateAttack works'''
		attack1 = [(5, 1), [(3, 3), (1, 5)]]
		attack2 = [(5, 1), [(3, 3)]]

		self.assertEquals(self.testObject.evaluateAttack(attack1), 2)
		self.assertEquals(self.testObject.evaluateAttack(attack2), 1)

	def test_generateStimulus(self):
		'''StaticAI.generateStimulus works'''
		move1 = [(5, 1), (4, 2)]
		stimulus1 = np.asarray([
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 3, 0, 0, 0, 0, 0],
			[0, 2, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0]
			], dtype = config.STORAGE_DATATYPE)

		move2 = [(7, 0), [(5, 2), (3, 4), (1, 2)]]
		stimulus2 = np.asarray([
			[0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 3, 0, 0, 0, 0, 0],
			[0, 0, 0, 1, 0, 0, 0, 0],
			[0, 0, 0, 0, 3, 0, 0, 0],
			[0, 0, 0, 1, 0, 0, 0, 0],
			[0, 0, 3, 0, 0, 0, 0, 0],
			[0, 1, 0, 0, 0, 0, 0, 0],
			[2, 0, 0, 0, 0, 0, 0, 0]
			], dtype = config.STORAGE_DATATYPE)

		self.assertEquals(self.testObject.generateStimulus(move1), stimulus1)
		self.assertEquals(self.testObject.generateStimulus(move2), stimulus2)

	def test_makeMove(self):
		'''StaticAI.makeMove works'''
		state = np.asarray([
			[0, 1, 0, 1, 0, 1, 0, 1],
			[0, 0, 1, 0, 1, 0, 1, 0],
			[0, 1, 0, 0, 0, 1, 0, 0],
			[1, 0, 0, 0, 0, 0, 1, 0],
			[0, 1, 0, 0, 0, 2, 0, 0],
			[2, 0, 2, 0, 2, 0, 0, 0],
			[0, 2, 0, 2, 0, 2, 0, 2],
			[2, 0, 2, 0, 2, 0, 2, 0]
			], dtype = config.STORAGE_DATATYPE)

		possibleMoves = [
			[(5, 0), [(3, 2), (1, 0)]],
			[(5, 0), [(3, 2)]],
			[(4, 5), [(2, 7)]]
			]

		self.testObject.possibleStimuli = []
		self.testObject.setState(state)

		success, playedMove = self.testObject.makeMove()
		matchedRule = self.connection.Rule.find_one({"response": playedMove})

		self.assertTrue(success)
		self.assertIn(playedMove, possibleMoves)
		self.assertEquals(matchedRule["response"], playedMove)

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
				[0, 0, 0, 1, 0, 0, 0, 0]
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
