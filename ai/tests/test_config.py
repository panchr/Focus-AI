# Rushy Panchal
# ai/tests/test_config.py

import unittest
import baseTests

import config

class TestConfig(unittest.TestCase, baseTests.BaseTest, object):
	'''Test the configuration'''

	@unittest.skipIf(not config.DEV_MODE, "development mode")
	def test_devEnv(self):
		'''development environment settings are correct'''
		self.assertEquals(config.DB_HOST, "localhost")
		self.assertEquals(config.DB_PORT, 27017)

		self.assertEquals(config.APP_HOST, "127.0.0.1")
		self.assertEquals(config.APP_PORT, 7337)
