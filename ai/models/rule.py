# Rushy Panchal
# ai/models/rule.py

from models.model import Model
from models.state import Gamestate
from models.condition import Condition
from models.response import Response

from mongokit import ConnectionError

import config

class Rule(Model):
	'''A general model for a Dynamic Scripting Rule'''
	__collection__ = "rulebase"

	structure = {
		"state": Gamestate(),
		"condition": Condition(),
		"response": Response(),
		"piece": int,
		"group": basestring,
		"weight": float, # although weights are initially stored as integers, they are occasionally changed to floats so that they can be normalized
		}
	
	required_fields = ["state", "condition", "response", "piece", "group", "weight"]

	default_values = {
		"weight": 0.0,
		"group": ""
		}

	@staticmethod
	def new(state, condition, response, piece = None, group = "", initialWeight = None):
		'''Creates a new rule'''
		rule = Model.connection.Rule()
		rule.state = state
		rule.condition = condition
		rule.response = response
		if piece is None:
			piece = state[response[0]] if len(response) > 0 else 0
		rule.piece = piece
		rule.group = group
		if initialWeight is not None:
			rule.weight = initialWeight
		rule.save()
		return rule

	@Model.autosave
	def increaseWeight(self, group = True):
		'''Increments the weight'''
		self.weight += config.WEIGHT_DELTA
		if group and self.group: # if the group is not empty (because empty groups aren't shared)
			self.collection.update({"group": self.group}, {"$inc": {"weight": config.WEIGHT_DELTA}}, multi = True)
			# update the weights of this group as well
		if (self.weight + 1) >= config.NORMALIZE_THRESHOLD:
		# if the weight exceeds the threshold, normalize all of the values
			Rule.normalize()

	@Model.autosave
	def decreaseWeight(self, group = True):
		'''Decreases the weight
		Similar to Rule.increaseWeight except with a negative delta value.'''
		self.weight -= config.WEIGHT_DELTA
		if group and self.group:
			self.collection.update({"group": self.group}, {"$inc": {"weight": -1 * config.WEIGHT_DELTA}}, multi = True)
		if (self.weight - 1) <= config.NORMALIZE_THRESHOLD_NEG:
			Rule.normalize()

	@classmethod
	def normalize(cls):
		'''Normalizes all of the weights between 0 and 1'''
		rules = list(cls.connection.Rule.find())
		sumWeights = float(sum(map(lambda rule: rule.weight, rules)))
		for rule in rules:
			rule.weight = rule.weight / sumWeights
			rule.save()
