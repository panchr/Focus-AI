# Rushy Panchal
# ai/models/game.py

from bson.objectid import ObjectId

from models.model import Model
from models.state import Gamestate

class Game(Model):
	'''Contains all of the data about a single game that was played'''
	__collection__ = "games"

	structure = {
		"players": [ObjectId], # User.id
		"history": [Gamestate()], # should be [Gamestate], but Mongokit throws a SchemaError --- this works so Gamestate is definitely a valid type
		"rulesUsed": [ObjectId], # Rule.id, only needed if AI
		"feedback": basestring,
		}

	required = ["players", "history", "feedback"]
