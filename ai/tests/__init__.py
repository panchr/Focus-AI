# Rushy Panchal
# tests/__init__.py

import os
import sys

# Set up database connection for the unit tests
import subprocess

from baseTests import TEST_HOST, TEST_PORT, GENERATED_COLLECTIONS
from pymongo.errors import ConnectionFailure
from mongokit import Connection

devNull = None
devServer = None

def setup():
	'''Set up the test package'''
	global devServer, devNull
	sys.path.append(os.path.join(os.path.abspath("."), "tests"))
	
	devNull = open(os.devnull, "wb")
	devServer = subprocess.Popen(["mongod"], stdout = devNull)

	try:
		connection = Connection(host = TEST_HOST, port = TEST_PORT)
		if connection.server_info()["ok"] == 1.0:
			connection.close()
			return True # abort any other actions because connection is successful
	except ConnectionFailure:
		pass

	# This is only run if the connection was not successful
	teardown()
	sys.exit("Could not connect to the MongoDB database")
	return False

def teardown():
	'''Tear down the test package'''
	conn = Connection(host = TEST_HOST, port = TEST_PORT)

	for db, coll in GENERATED_COLLECTIONS:
		conn[db].drop_collection(coll)

	if devServer:
		devServer.kill()
	if devNull:
		devNull.close()
