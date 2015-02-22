# Rushy Panchal
# ai/core/__init__.py

from core.database import Database
from models.user import User
from models.rule import Rule

from core.dev import DevelopmentServer

import atexit
import os

import config

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

	return db

if __name__ == '__main__':
	start()
