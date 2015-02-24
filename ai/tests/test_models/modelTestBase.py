# Rushy Panchal
# tests/test_models/modelTestBase.py

import unittest
import baseTests
import types

from mongokit import Document, CustomType, ConnectionError

VALID_MONGOKIT_TYPES = Document.authorized_types

class ModelTestBase(baseTests.BaseTest, object):
	'''Base testing class for Models'''
	def test_isSubclass(self):
		'''subclass of Document'''
		self.assertIsSubclass(self.model, Document)

	def test_instanceOf(self):
		'''instanceof Document'''
		self.assertIsInstance(self.modelObject, Document)

	def test_hasDatabase(self):
		'''Database defined'''
		self.assertHasAttr(self.modelObject, "__database__")
		self.assertIsInstance(self.modelObject.__database__, str)
	
	def test_hasCollection(self):
		'''Collection defined'''
		self.assertHasAttr(self.modelObject, "__collection__")
		self.assertIsInstance(self.modelObject.__collection__, str)

	def test_hasStructure(self):
		'''Structure defined'''
		self.assertHasAttr(self.modelObject, "structure")
		self.assertIsInstance(self.modelObject.structure, dict)

	def test_validStructure(self):
		'''Structure valid'''
		self.assertTrue(self.validateMongokit(self.modelObject.structure), "structure not valid")

	def test_requiredValues(self):
		'''Required values exist in structure'''
		if (hasattr(self.modelObject, "required")):
			all_values = self.flattenDict(self.modelObject.structure)
			for value in self.modelObject.required:
				self.assertIn(value, all_values)

	def test_defaultValues(self):
		'''Default values exist in structure'''
		if (hasattr(self.modelObject, "default_values")):
			for value in self.modelObject.default_values.keys():
				value_type = self.accessFlattened(self.modelObject.structure, value)
				self.assertIsInstance(
					self.modelObject.default_values[value],
					value_type if isinstance(value_type, type) else type(value_type))

	def test_dotNotation(self):
		'''Dot notation is enabled'''
		self.assertHasAttr(self.modelObject, "use_dot_notation")
		self.assertTrue(self.modelObject.use_dot_notation)

	# Helper functions
	def validateMongokit(self, dictionary, baseKey = "", errors = None):
		'''Validate a MongoKit structure dictionary'''
		valid = True
		if not errors:
			errors = []
		for (key, dataType) in dictionary.iteritems():
			typeValid = self.validateMongokitItem(
				"{base}.{minor}".format(base = baseKey, minor = key) if baseKey else key,
				dataType, errors)
			valid = (valid and typeValid)
		if (not valid):
			self.fail("\n{errors}".format(errors = "\n".join(errors))) # report all errors
		return valid

	def validateMongokitItem(self, key, item, errors):
		'''Validate a single Mongokit item'''
		if (item in VALID_MONGOKIT_TYPES):
			return True
		elif (isinstance(item, dict)):
			return self.validateMongokit(item, key, errors) # if it is a dictionary, recursively validate that as well
		elif (isinstance(item, list)):
			if (len(item) == 0): # an empty list is always valid
				return True
			elif (len(item) == 1): # if it's a single-item-list, make sure that item is valid
				return self.validateMongokitItem(key, item[0], errors)
		elif (isinstance(item, CustomType) or issubclass(item, CustomType)): # a CustomType must be valid
			return True
		else:
			errors.append("\t{key}, {dataType} is not a valid Mongokit data type.".format(key = key, dataType = item))
			return False

class CustomTypeTestBase(baseTests.BaseTest, object):
	'''Testing class for CustomTypes'''
	def test_isSubclass(self):
		'''subclass of CustomType'''
		self.assertIsSubclass(self.model, CustomType)

	def test_instanceOf(self):
		'''instanceof CustomType'''
		self.assertIsInstance(self.modelObject, CustomType)

	def test_hasMongoType(self):
		'''mongo_type is set'''
		self.assertHasAttr(self.modelObject, "mongo_type")
		self.assertTrue(self.modelObject.mongo_type in VALID_MONGOKIT_TYPES or type(self.modelObject.mongo_type) in VALID_MONGOKIT_TYPES)

	def test_hasPythonType(self):
		'''python_type is set'''
		self.assertHasAttr(self.modelObject, "python_type")

	def test_hasInitType(self):
		'''init_type is set'''
		self.assertHasAttr(self.modelObject, "init_type")
		self.assertIn(self.modelObject.init_type, (self.modelObject.python_type, type(self.modelObject.python_type), types.NoneType, None))

	def test_hasToPython(self):
		'''to_python method is set'''
		self.assertFunctionExists(self.modelObject, "to_python")

	def test_hasToBson(self):
		'''to_bson method is set'''
		self.assertFunctionExists(self.modelObject, "to_bson")

	def test_toBson(self):
		'''Python to BSON conversions'''
		for (bson, python) in self.mongoConversions:
			bson_raw = self.modelObject.to_bson(python)
			self.assertEquals(bson_raw, bson)
			self.assertIsInstance(bson_raw, type(bson))

	def test_toPython(self):
		'''BSON to Python conversions'''
		for (bson, python) in self.mongoConversions:
			python_raw = self.modelObject.to_python(bson)
			self.assertEquals(python_raw, python)
			self.assertIsInstance(python_raw, type(python))
