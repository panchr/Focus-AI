# Rushy Panchal
# ai/core/__init__.py

import core
import models

import atexit
import os

import config

engine = None
db = None

def start():
	'''Starts the core features'''
	if (config.DEV_MODE):
		devServer = core.dev.DevelopmentServer()
		devServer.start()
		atexit.register(devServer.stop)

	db = core.database.Database(host = config.HOST, port = config.PORT)
	db.register([
		models.User,
		models.Rule,
		models.Game
		])
	models.register(db)
	engine = core.engine.Engine(database = db)

	return engine, db

if __name__ == '__main__':
	engine, db = start()
