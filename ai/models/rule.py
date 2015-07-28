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
		"strength": float, # the strength is how good the move is
		"combinedWeight": float, # the combined weights of each group
		}
	
	required_fields = ["state", "condition", "response", "piece", "group", "weight", "strength", "combinedWeight"]

	default_values = {
		"group": "",
		"weight": 0.0,
		"strength": 0.0,
		"combinedWeight": 0.0,
		}

	@staticmethod
	def new(state, condition, response, piece = None, group = "", initialWeight = None, initialStrength = None):
		'''Creates a new rule'''
		rule = Model.connection.Rule()

		rule.state = state
		rule.condition = condition
		rule.response = response

		if piece is None:
			piece = int(state[response[0]]) if len(response) > 0 else 0
			# must explicitly convert to int to store in MongoDB

		rule.piece = piece
		rule.group = group
		combinedWeight = 0

		if initialWeight is not None:
			rule.weight = initialWeight
			combinedWeight += initialWeight
		if initialStrength is not None:
			rule.strength = initialStrength
			combinedWeight += initialStrength
		if combinedWeight:
			rule.combinedWeight = combinedWeight

		rule.save()
		return rule

	def deltaField(self, field = "weight", delta = config.WEIGHT_DELTA, group = True):
		'''Change the weight or strength of the field'''
		self[field] += delta
		self.combinedWeight += delta
		if group and self.group: # if the group is not empty (because empty groups aren't shared)
			self.collection.update({"group": self.group}, {"$inc": {field: delta, "combinedWeight": delta}}, multi = True)
			# update the weights or strengths of this group as well

		if (((self[field] + 1) > config.NORMALIZE_THRESHOLD) or
			((self[field] - 1) < config.NORMALIZE_THRESHOLD_NEG) or
			((self.combinedWeight + 1) > config.NORMALIZE_THRESHOLD) or
			((self.combinedWeight - 1) < config.NORMALIZE_THRESHOLD_NEG)):
			# if the weight or strength is close to breaking the max or min integer, normalize all of the weights
			Rule.normalize()

	@Model.autosave
	def increaseWeight(self, group = True):
		'''Increments the weight''',
		return self.deltaField(field = "weight", delta = config.WEIGHT_DELTA, group = group)

	@Model.autosave
	def decreaseWeight(self, group = True):
		'''Decreases the weight
		Similar to Rule.increaseWeight except with a negative delta value.'''
		return self.deltaField(field = "weight", delta = -1 * config.WEIGHT_DELTA, group = group)

	@Model.autosave
	def increaseStrength(self, group = True):
		'''Increments the strength'''
		return self.deltaField(field = "strength", delta = config.WEIGHT_DELTA, group = group)

	@Model.autosave
	def decreaseStrength(self, group = True):
		'''Decreases the strength
		Similar to Rule.increaseStrength except with a negative delta value.'''
		return self.deltaField(field = "strength", delta = -1 * config.WEIGHT_DELTA, group = group)

	@classmethod
	def normalize(cls):
		'''Normalizes all of the weights and strengths between 0 and 1'''
		rules = list(cls.connection.Rule.find())

		sumWeights = float(sum(map(lambda rule: rule.weight, rules))) or 1 # the "or 1" makes sure we don't get a division by zero error
		sumStrengths = float(sum(map(lambda rule: rule.strength, rules))) or 1
		sumCombinedWeights = sumWeights + sumStrengths

		for rule in rules:
			rule.weight = rule.weight / sumWeights
			rule.strength = rule.strength / sumStrengths
			rule.combinedWeight = rule.combinedWeight / sumCombinedWeights
			rule.save()
