# Rushy Panchal
# ai/models/game.py

from bson.objectid import ObjectId

from models.model import Model
from models.state import Gamestate

import datetime

class Game(Model):
	'''Contains all of the data about a single game that was played'''
	__collection__ = "history"

	structure = {
		"history": [Gamestate()],
		"rules": [ObjectId], # Rule.id, only needed if AI
		"feedback": basestring,
		"seemedHuman": bool,
		"timestamp": datetime.datetime
		}

	required = ["rules", "history", "feedback", "seemedHuman", "timestamp"]

	default_values = {
		"feedback": "",
		"seemedHuman": False,
		"history": [],
		"rules": []
		}

	@staticmethod
	def new(history, rules, feedback, seemedHuman):
		'''Store a new record in the history'''
		record = Model.connection.Game()
		record.history = history
		record.rules = rules
		record.feedback = feedback
		record.seemedHuman = seemedHuman
		record.timestamp = datetime.datetime.now()

		record.save()

		return record
