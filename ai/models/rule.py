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
		"weight": int,
		}
	
	required_fields = ["state", "weight", "condition", "response"]

	@Model.autosave
	def increase_weight(self):
		'''Increments the weight'''
		self.weight += 1

	@Model.autosave
	def decrease_weight(self):
		'''Decreases the weight'''
		self.weight -= 1
