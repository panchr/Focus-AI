# Rushy Panchal
# ai/core/__init__.py

from core.database import Database
from models.user import User
from models.rule import Rule

from core.dev import DevelopmentServer
import atexit

from config import *

if (DEV_MODE):
	devServer = DevelopmentServer()
	devServer.start()

db = Database("localhost", 27017)
db.setup([
	User,
	Rule
	])

atexit.register(devServer.stop)
