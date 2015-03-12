# Rushy Panchal
# tests/models/test_game.py

import unittest
import baseTests

from modelTestBase import ModelTestBase
from models.game import Game

class TestGame(ModelTestBase, unittest.TestCase):
	'''Tests the models.game.Game Model'''
	model = Game
