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
		self.assertEquals(config.HOST, "localhost")
		self.assertEquals(config.PORT, 27017)
