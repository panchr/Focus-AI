# Rushy Panchal
# ai/core/route.py

import json

from core.response import Response
from core.errors import MalformedQuery, InvalidMove, WrongPlayerMove
from core.artificial import DynamicScriptingAI

import random

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
		response = ROUTES[data["action"]](db, engine, data["data"])
		return msg_id, response
	except KeyError:
		return msg_id, Response.error(MalformedQuery("action or data field not provided"))

def newGame(db, engine, data):
	'''Create a new game'''
	gameID = engine.newGame()
	playerPiece = random.randint(1, 2)
	aiPiece = 2 if playerPiece == 1 else 1
	ai = DynamicScriptingAI(db, engine, gameID, aiPiece)
	ALL_AI[gameID] = ai
	return Response.json("Game created", "Success", 200, gameID = gameID, piece = playerPiece)

def makeMove(db, engine, data):
	'''Make the game move'''
	gameID = data["gameID"]
	move = data["move"]

	try:
		valid, pieces, winner, upgraded = engine.makeMove(gameID, *move)
	except InvalidMove:
		return Response.json("Invalid Move", "Move Error", 401)
	except WrongPlayerMove:
		return Response.json("Not Your Turn", "Wrong Player", 409)

	if winner:
		return Response.json("Game end", "Success", 201, winner = winner, pieces = pieces, upgraded = upgraded)

	return Response.json("Move executed", "Success", 200, pieces = pieces, upgraded = upgraded)

def makeMoveAI(db, engine, data):
	'''Make the AI game move'''
	gameID = data["gameID"]
	move, success, pieces, winner, upgraded = ALL_AI[gameID].makeMove()
	
	if winner:
		return Response.json("Game end", "Success", 201, winner = winner, pieces = pieces, move = move, upgraded = upgraded)

	return Response.json("Move executed", "Success", 200, move = move, pieces = pieces, upgraded = upgraded)

ROUTES = {
	"game.new": newGame,
	"game.move": makeMove,
	"game.ai.move": makeMoveAI
	}
