# Rushy Panchal
# tests/models/test_auth.py

import unittest
import baseTests

from modelTestBase import CustomTypeTestBase
from models.auth import HashedPassword

class TestAuth(CustomTypeTestBase, unittest.TestCase):
	'''Tests the models.auth.Auth Model'''
	model = HashedPassword
	mongoConversions = [
		("focus-ai", "focus-ai"),
		("testcase2", "testcase2"),
		("randomSpamTest", "randomSpamTest")
		]

	def setUp(self):
		'''Set up the test case'''
		self.modelObject = self.model()
		self.baseSalt = "$2a$12$NwZuVdNNB8l2jSaGzZvwIO"
		self.hashes = {
			"cryptosana": "$2a$12$NwZuVdNNB8l2jSaGzZvwIOTMuJNte9bRc6NIkf.CTmpuoEIaXVqPS",
			"rushypanchal": "$2a$12$NwZuVdNNB8l2jSaGzZvwIOEtuuXyg.AuJz4h6SZh/8mM5ytfo06na",
			"RaNDoMTestCas3": "$2a$12$NwZuVdNNB8l2jSaGzZvwIOK8NsTRDB6QNE75C5Q0DUa39NMjtJYki"
			}

	@unittest.skipIf(baseTests.dev, "development mode")
	def test_passwordHash(self):
		'''Password hash works'''
		for (password, hashed) in self.hashes.iteritems():
			self.assertEquals(HashedPassword.hash(password, self.baseSalt), hashed)
	
	@unittest.skipIf(baseTests.dev, "development mode")
	def test_passwordCheck(self):
		'''Password checking works'''
		for (password, hashed) in self.hashes.iteritems():
			self.assertTrue(HashedPassword.check(password, hashed), "passwords do not much")
