# Rushy Panchal
# ai/core/generate-rules.py

import numpy as np
import json
import copy

from core.database import Database
from core.dev import DevelopmentServer
import models

import config

RESPONSE_CONVERTER = models.response.Response()

def main():
	'''Main process'''
	if config.DEV_MODE:
		devServer = DevelopmentServer()
		devServer.start()
	else:
		devServer = None

	db = Database(host = config.DB_HOST, port = config.DB_PORT)
	db.register(models.Rule)
	models.register(db)

	try:
		with open("rules.json", "r") as rulesFile:
			ruleData = json.load(rulesFile)

		rules = []

		for rule in ruleData:
			state = np.asarray(rule["state"], dtype = config.STORAGE_DATATYPE)
			condition = np.asarray(rule["condition"], dtype = config.STORAGE_DATATYPE)
			response, piece = rule["response"], rule["piece"]

			flippedRule = changeRulePiece(state, condition, response, piece, rule.get('initialWeight', None))
			rules.append(flippedRule)

			state[condition != 0] = 0
			state |= condition
			state[state == 3] = 0

			rule["condition"] = condition
			rule["state"] = state

			rules.append(rule)

			# should also test the translations of these rules

		for rule in rules:
			print rule
			#db.newRule(**rule)
			print("Rule {n} added".format(n = id(rule)))
	except WindowsError:
		pass

	if devServer:
		devServer.stop()
		devServer = None
	db.close()

	return True

def changeRulePiece(state, condition, response, piece, initialWeight = None):
	'''Changes the board structure so that it works for a different piece'''
	state, condition, response = map(copy.deepcopy, [state, condition, response])
	newRule = {}
	condition = condition[::-1, ::-1]

	flipPieces(condition)

	state[condition != 0] = 0
	state |= condition
	state[state == 3] = 0

	newRule["state"] = state
	newRule["condition"] = condition
	newRule["response"] = flipResponse(response, *state.shape)
	newRule["piece"] = (1 if piece == 2 else 2)
	if initialWeight:
		newRule["initialWeight"] = initialWeight

	return newRule

def flipPieces(matrix):
	'''Flips the pieces in the matrix'''
	matrix[matrix == 1] = 100 # temporary value
	matrix[matrix == -1] = -100 # temporaryvalue

	# 2 ---> 1
	matrix[matrix == 2] = 1
	matrix[matrix == -2] = -1

	# 1 ---> 2
	matrix[matrix == 100] = 2
	matrix[matrix == -100] = -2

	return matrix

def flipResponse(resp, h, w):
	'''Flip the response to match the new coordinates'''
	resp = RESPONSE_CONVERTER.to_python(resp)

	flipIndividual = lambda coord: (h - coord[0] - 1, w - coord[1] - 1)

	resp[0] = flipIndividual(resp[0])
	if isinstance(resp[1], list):
		resp[1] = map(flipIndividual, resp[1])
	else:
		resp[1] = flipIndividual(resp[1])

	return resp

if __name__ == '__main__':
	main()
