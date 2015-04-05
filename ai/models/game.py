# Rushy Panchal
# ai/models/game.py

from bson.objectid import ObjectId

from models.model import Model
from models.state import Gamestate

class Game(Model):
	'''Contains all of the data about a single game that was played'''
	__collection__ = "history"

	structure = {
		"history": [Gamestate()],
		"rules": [ObjectId], # Rule.id, only needed if AI
		"feedback": basestring,
		"seemedHuman": bool
		}

	required = ["rules", "history", "feedback", "seemedHuman"]

	default_values = {
		"feedback": "",
		"seemedHuman": False,
		"history": [],
		"rules": []
		}
