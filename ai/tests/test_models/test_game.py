# Rushy Panchal
# tests/models/test_game.py

import unittest
import baseTests

from modelTestBase import ModelTestBase
from models.game import Game

class TestGame(unittest.TestCase, ModelTestBase):
	'''Tests the models.game.Game Model'''
	def setUp(self):
		'''Set up the test case'''
		self.model =  Game
		self.modelObject = self.model()
