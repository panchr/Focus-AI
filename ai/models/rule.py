# Rushy Panchal
# ai/models/rule.py

from model import Model

class Rule(Model):
	'''A general model for a Dynamic Scripting Rule'''
	__collection__ = "rulebase"

	structure = {
		"state": basestring,
		"weight": int,
		"condition": basestring,
		"response": basestring,
		}
	
	required_fields = ["state", "weight", "condition", "response"]
