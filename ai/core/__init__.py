# Rushy Panchal
# ai/core/__init__.py

from core.database import Database
from core.engine import Engine
from models.user import User
from models.rule import Rule

from core.dev import DevelopmentServer

import atexit
import os

import config

engine = None
db = None

def start():
	'''Starts the core features'''
	if (config.DEV_MODE):
		devServer = DevelopmentServer()
		devServer.start()
		atexit.register(devServer.stop)

	db = Database(host = config.HOST, port = config.PORT)
	db.register([
		User,
		Rule
		])
	engine = Engine()

	return engine, db

if __name__ == '__main__':
	engine, db = start()
