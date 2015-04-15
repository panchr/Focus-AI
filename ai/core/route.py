# Rushy Panchal
# ai/core/route.py

import json

from core.response import Response
from core.errors import MalformedQuery, InvalidMove, WrongPlayerMove

ALL_AI = {}

def routeRequest(db, engine, data):
	'''Routes the request'''
	try:
		data = json.loads(data)
		msg_id = data["msg_id"]
	except ValueError:
		return "", Response.error(MalformedQuery("JSON could not be decoded"))
	except KeyError:
		return "", Response.error(MalformedQuery("msg_id field could not be found"))

	try:
		response = ROUTES[data["action"]](engine, data["data"])
		return msg_id, response
	except KeyError:
		return msg_id, Response.error(MalformedQuery("action or data field not provided"))

def newGame(db, engine, data):
	'''Create a new game'''
	# need to choose a piece for the player and for the AI
	
	gameID = engine.newGame()
	return Response.json("Game created", "Success", 200, gameID = gameID)

def makeMove(db, engine, data):
	'''Make the game move'''
	gameID = data["gameID"]
	move = data["move"]

	try:
		valid, pieces, winner = engine.makeMove(gameID, *move)
	except InvalidMove:
		return Response.json("Invalid Move", "Move Error", 401)
	except WrongPlayerMove:
		return Response.json("Not Your Turn", "Wrong Player", 409)

	return Response.json("Move executed", "Success", 200)

def makeMoveAI(db, engine, data):
	'''Make the AI game move'''
	gameID = data["gameID"]
	success, move = ALL_AI[gameID].makeMove()

	return Response.json("Move executed", "Success", 200, move = move)

ROUTES = {
	"game.new": newGame,
	"game.move": makeMove,
	"game.ai.move": makeMoveAI
	}
