# Rushy Panchal
# ai/models/game.py

from bson.objectid import ObjectId

from models.model import Model

class Game(Model):
	'''Contains all of the data about a single game that was played'''
	structure = {
		"players": [ObjectId], # Player.id
		"history": [Gamestate],
		"rulesUsed": [ObjectId], # Rule.id, only needed if AI
		"feedback": Feedback,
		}

	required = ["players", "history", "feedback"]
