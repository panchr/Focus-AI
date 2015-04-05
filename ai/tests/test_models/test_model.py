# Rushy Panchal
# ai/tests/models/test_model.py

import unittest
import baseTests

import mongokit

from models.model import Model
from models.model import CustomTypeBase

class TestModel(baseTests.BaseTest, unittest.TestCase):
	'''Tests the base Model class'''
	base = Model

	def test_hasDefaultConfig(self):
		'''Default configuration values exist'''
		self.assertHasAttr(self.base, "__database__")
		self.assertHasAttr(self.base, "use_dot_notation")
		self.assertHasAttr(self.base, "skip_validation")
		self.assertHasAttr(self.base, "connection")

	def test_defaultConfig(self):
		'''Default configuration values are set to the correct values'''
		self.assertEquals(self.base.__database__, "senior_focus")
		self.assertEquals(self.base.use_dot_notation, True)
		self.assertEquals(self.base.skip_validation, True)

	def test_inheritsDocument(self):
		'''inherits from Document'''
		self.assertIsSubclass(self.base, mongokit.Document)
		self.assertIsSubclass(self.base, object)

	def test_hasAutosave(self):
		'''Model.autosave exists'''
		self.assertFunctionExists(self.base, "autosave")

	def test_hasNew(self):
		'''Model.new exists'''
		self.assertFunctionExists(self.base, "new")

	def test_autosave(self):
		'''Model.autosave works'''
		pass # not implemented yet

	def test_new(self):
		'''Model.new works'''
		pass # not implemented yet

class TestCustomTypeBase(baseTests.BaseTest, unittest.TestCase):
	'''Tests the CustomTypeBase class'''
	base = CustomTypeBase

	def test_hasDefaultConfig(self):
		'''Default configuration values exist'''
		self.assertHasAttr(self.base, "mongo_type")
		self.assertHasAttr(self.base, "python_type")
		self.assertHasAttr(self.base, "init_type")

	def test_defaultConfig(self):
		'''Default configuration values are set to the correct values'''
		self.assertEquals(self.base.mongo_type, None)
		self.assertEquals(self.base.python_type, None)
		self.assertEquals(self.base.init_type, None)

	def test_inheritsCustomType(self):
		'''inherits from Document'''
		self.assertIsSubclass(self.base, mongokit.CustomType)
		self.assertIsSubclass(self.base, object)

	def test_hasToBson(self):
		'''CustomTypeBase.to_bson exists'''
		self.assertFunctionExists(self.base, "to_bson")

	def test_hasToPython(self):
		'''CustomTypeBase.to_python exists'''
		self.assertFunctionExists(self.base, "to_python")
