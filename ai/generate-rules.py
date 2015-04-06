# Rushy Panchal
# ai/core/generate-rules.py

import numpy as np
import json
import copy

from core.database import Database
from core.dev import DevelopmentServer
import models

import config

response_to_tuple = models.response.Response().to_python

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
			response, piece = response_to_tuple(rule["response"]), rule["piece"]

			flippedRule = changeRulePiece(state, condition, response, piece, rule.get('initialWeight', None))
			translated = translateRule(state, condition, response, piece, rule.get('initialWeight', None))
			translatedFlipped = translateRule(flippedRule["state"], flippedRule["condition"], flippedRule["response"], flippedRule["piece"], rule.get('initialWeight'))

			state = mergeCondition(state ,condition)
			rule["condition"] = condition
			rule["state"] = state
			rule["response"] = response

			rules.append(rule)
			rules.append(flippedRule)
			rules.extend(translated)
			rules.extend(translatedFlipped)

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

	state = mergeCondition(state, condition)

	newRule["state"] = state
	newRule["condition"] = condition
	newRule["response"] = flipResponse(response, *state.shape)
	newRule["piece"] = (1 if piece == 2 else 2)
	if initialWeight is not None:
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
	flipIndividual = lambda coord: (h - coord[0] - 1, w - coord[1] - 1)

	resp[0] = flipIndividual(resp[0])
	if isinstance(resp[1], list):
		resp[1] = map(flipIndividual, resp[1])
	else:
		resp[1] = flipIndividual(resp[1])

	return resp

def mergeCondition(state, condition):
	'''Merge the condition into the state'''
	state[condition != 0] = 0
	state |= condition
	state[state == 3] = 0
	return state

def translateRule(state, condition, response, piece, initialWeight = None):
	'''Translates a rule to match new positions'''
	changeNum = lambda delta: lambda n: n + delta
	translated = []

	isTake = isinstance(response[1], list)

	condY, condX = np.where(condition > 0)
	if isTake:
		respY = [response[0][0]] + [pos[0] for pos in response[1]]
		respX = [response[0][1]] + [pos[1] for pos in response[1]]
	else:
		respY, respX = [pos[0] for pos in response], [pos[1] for pos in response]

	maxY, maxX = map(changeNum(-1), condition.shape)

	for deltaY in xrange(-6, 7, 2):
		for deltaX in xrange(-6, 7, 2):
			if deltaX == 0 and deltaY == 0:
				continue # this would duplicate the original rule
			if all(map(all, [
				map(lambda y: (0 <= y < maxY), map(changeNum(deltaY), condY)),
				map(lambda x: (0 <= x < maxX), map(changeNum(deltaX), condX)),
				map(lambda y: (0 <= y < maxY), map(changeNum(deltaY), respY)),
				map(lambda x: (0 <= x < maxX), map(changeNum(deltaX), respX)),
				])):
				translatedCond = np.roll(np.roll(condition, deltaY, axis = 0), deltaX, axis = 1)
				translatedResp = [(response[0][0] + deltaY, response[0][1] + deltaX)]
				translatedResp.append(
					map(lambda pos: (pos[0] + deltaY, pos[1] + deltaX), response[1]) if isTake else (response[1][0] + deltaY, response[1][1] + deltaX)
					)
				translatedRule = {
					"condition": translatedCond,
					"state": mergeCondition(copy.copy(state), translatedCond),
					"response": translatedResp,
					"piece": piece
					}
				if initialWeight is not None:
					translatedRule["initialWeight"] = initialWeight

				translated.append(translatedRule)
			
	return translated

if __name__ == '__main__':
	main()
