# Rushy Panchal
# ai/core/generate-rules.py

import numpy as np
import json
import copy
import pprint

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

		output = ""
		rules = []

		for rule in ruleData:
			state = np.asarray(rule["state"] if rule["state"] else defaultState(), dtype = config.STORAGE_DATATYPE)
			condition = np.asarray(rule["condition"], dtype = config.STORAGE_DATATYPE)
			response, piece = response_to_tuple(rule["response"]), rule["piece"]

			initialWeight = rule.get('initialWeight', None)

			# Calculate the flipped and translated values
			flippedRule = changeRulePiece(state, condition, response, piece, initialWeight)
			translated = translateRule(state, condition, response, piece, initialWeight)
			translatedFlipped = translateRule(flippedRule["state"], flippedRule["condition"], flippedRule["response"], flippedRule["piece"], initialWeight)

			# Get the reflected values (and then the flipped and translated for the reflected)
			reflectedRule = reflectRule(state, condition, response, piece, initialWeight)
			flippedReflected = changeRulePiece(reflectedRule["state"], reflectedRule["condition"], reflectedRule["response"], reflectedRule["piece"], initialWeight)
			translatedReflected = translateRule(reflectedRule["state"], reflectedRule["condition"], reflectedRule["response"], reflectedRule["piece"], initialWeight)
			translatedReflectedFlipped = translateRule(flippedReflected["state"], flippedReflected["condition"], flippedReflected["response"], flippedReflected["piece"], initialWeight)

			# Set the initial values for the condit
			state = mergeCondition(state ,condition)
			rule["condition"] = condition
			rule["state"] = state
			rule["response"] = response

			for baseRule, translatedRule in zip([rule, flippedRule, reflectedRule, flippedReflected],
				[translated, translatedFlipped, translatedReflected, translatedReflectedFlipped]):
				rules.append(baseRule)
				rules.extend(translatedRule)

		for index, rule in enumerate(rules, 1):
			#db.newRule(**rule)
			addedOutput = "Rule {index} added: {n}".format(index = index, n = hex(id(rule)))
			print(addedOutput)
			output += "{base}\n{rule}\n".format(base = addedOutput, rule = pprint.pformat(rule))

		with open("generated-rules.output", "w") as outputFile:
			outputFile.write(output)

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
	condition = condition[::-1, ::-1]

	flipPieces(condition)

	state = mergeCondition(state, condition)

	newRule = {
		"state": state,
		"condition": condition,
		"response": flipResponse(response, *state.shape),
		"piece": (1 if piece == 2 else 2)
		}
	if initialWeight is not None:
		newRule["initialWeight"] = initialWeight

	return newRule

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
				map(lambda y: (0 <= y <= maxY), map(changeNum(deltaY), condY)),
				map(lambda x: (0 <= x <= maxX), map(changeNum(deltaX), condX)),
				map(lambda y: (0 <= y <= maxY), map(changeNum(deltaY), respY)),
				map(lambda x: (0 <= x <= maxX), map(changeNum(deltaX), respX)),
				])): # make sure the rule is still within the given bounds

				# Perform all the necessary translations
				translatedCond = np.roll(np.roll(condition, deltaY, axis = 0), deltaX, axis = 1)
				translatedResp = [(response[0][0] + deltaY, response[0][1] + deltaX)]
				translatedResp.append(
					map(lambda pos: (pos[0] + deltaY, pos[1] + deltaX), response[1]) if isTake else (response[1][0] + deltaY, response[1][1] + deltaX)
					)

				translatedRule = {
					"condition": translatedCond,
					"state": mergeCondition(copy.copy(state), translatedCond),
					"response": translatedResp,
					"piece": piece,
					}
				if initialWeight is not None:
					translatedRule["initialWeight"] = initialWeight

				translated.append(translatedRule)
			
	return translated

def reflectRule(state, condition, response, piece, initialWeight = None):
	'''Reflect the rule across the x-axis to get a mirror image'''
	state, condition, response = map(copy.deepcopy, [state, condition, response])
	condition = np.roll(condition[:, ::-1], -1, axis = 1)
	response = flipResponse(response, h = 0, w = state.shape[1] - 1)

	reflected= {
		"state": mergeCondition(state, condition),
		"condition": condition,
		"response": response,
		"piece": piece
		}
	if initialWeight is not None:
		reflected["initialWeight"] = initialWeight

	return reflected

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

def flipResponse(resp, h = 0, w = 0):
	'''Flip the response to match the new coordinates'''
	flipIndividual = lambda coord: ((h - coord[0] - 1) if h else coord[0], (w - coord[1] - 1) if w else coord[1])

	resp[0] = flipIndividual(resp[0])
	if isinstance(resp[1], list):
		resp[1] = map(flipIndividual, resp[1])
	else:
		resp[1] = flipIndividual(resp[1])

	return resp

def mergeCondition(state, condition):
	'''Merge the condition into the state'''
	state[condition != 0] = 0 # make room for the new pieces
	state |= condition # merge the condition into the state
	state[state == 3] = 0 # make sure any blank spots are set as such
	return state

def defaultState():
	'''Returns the default state - the basic board'''
	board = np.asarray([
		[0, 1, 0, 1, 0, 1, 0, 1],
		[1, 0, 1, 0, 1, 0, 1, 0],
		[0, 1, 0, 1, 0, 1, 0, 1],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[2, 0, 2, 0, 2, 0, 2, 0],
		[0, 2, 0, 2, 0, 2, 0, 2],
		[2, 0, 2, 0, 2, 0, 2, 0]
		], dtype = np.int32)
	return board

if __name__ == '__main__':
	main()
