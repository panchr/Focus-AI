# Rushy Panchal
# ai/models/rule.py

from models.model import Model
from models.state import Gamestate
from models.condition import Condition
from models.response import Response

class Rule(Model):
	'''A general model for a Dynamic Scripting Rule'''
	__collection__ = "rulebase"

	structure = {
		"state": Gamestate,
		"condition": Condition,
		"response": Response,
		"weight": int, # might want to store it as a double instead so that all the weights can be normalized (instead of -infinity to +infinity, weights are 0 to 1)
		}
	
	required_fields = ["state", "weight", "condition", "response"]

	default_values = {
		"weight": 0
		}

	@Model.autosave
	def increaseWeight(self):
		'''Increments the weight'''
		self.weight += 1

	@Model.autosave
	def decreaseWeight(self):
		'''Decreases the weight'''
		self.weight -= 1