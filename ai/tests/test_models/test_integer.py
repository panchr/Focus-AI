# Rushy Panchal
# tests/models/test_integer.py

import unittest
import baseTests

from models.integer import Integer, Long

class TestInteger(unittest.TestCase, baseTests.BaseTest):
	'''Test the models.integer.Integer Model'''
	model = Integer

	def setUp(self):
		'''Sets up the test cases'''
		self.testA = self.model(0b10100101)
		self.testB = self.model(0b0100100101011000)
		self.testC = self.model(0b10010110)

	def test_invert(self):
		'''invert, ~, operator works'''
		self.assertEquals(~self.testA, 0b01011010)
		self.assertEquals(~self.testB, 0b011011010100111)
		self.assertEquals(~self.testC, 0b01101001)

	def test_rcirc(self):
		'''Integer.rcirc works'''
		self.assertEquals(self.testA.rcirc(2), 0b01101001)
		self.assertEquals(self.testB.rcirc(24), 0b101011000100100)
		self.assertEquals(self.testC.rcirc(12), 0b01101001)
		self.assertEquals(self.testC.rcirc(16), 0b10010110)

	def test_lcirc(self):
		'''Integer.lcirc works'''
		self.assertEquals(self.testA.lcirc(2), 0b10010110)
		self.assertEquals(self.testB.lcirc(17), 0b010010101100010)
		self.assertEquals(self.testC.lcirc(5), 0b11010010)
		self.assertEquals(self.testC.lcirc(8), 0b10010110)

	def test_lshift(self):
		'''Integer << n works'''
		self.assertEquals(self.testA << 2, 0b1010010100)
		self.assertEquals(self.testB << 4, 0b01001001010110000000)
		self.assertEquals(self.testC << 0, 0b10010110)

	def test_rshift(self):
		'''Integer >> n works'''
		self.assertEquals(self.testA >> 2, 0b101001)
		self.assertEquals(self.testB >> 4, 0b010010010101)
		self.assertEquals(self.testC >> 0, 0b10010110)

	def test_and(self):
		'''Integer & Integer works'''
		self.assertEquals(self.testA & self.testC, 0b10000100)
		self.assertEquals(self.testC & self.testA, 0b10000100)

	def test_or(self):
		'''Integer | Integer works'''
		self.assertEquals(self.testA | self.testC, 0b10110111)
		self.assertEquals(self.testC | self.testA, 0b10110111)

	def test_xor(self):
		'''Integer ^ Integer works'''
		self.assertEquals(self.testA ^ self.testC, 0b00110011)
		self.assertEquals(self.testC ^ self.testA, 0b00110011)

	def test_moveBit(self):
		'''Integer.moveBit works'''
		self.assertEquals(self.testA.moveBit(5, 1), 0b10000111)
		self.assertEquals(self.testB.moveBit(3, 5), 0b0100100101110000)
		self.assertEquals(self.testC.moveBit(0, 0), 0b10010110)

	def test_concat(self):
		'''Integer.concat works'''
		self.assertEquals(self.testA.concat(self.testC), 0b1010010110010110)
		self.assertEquals(self.testC.concat(self.testA), 0b1001011010100101)
		self.assertEquals(self.testB.concat(self.testB), 0b0100100101011000100100101011000)
		self.assertEquals(self.testA.concat(self.testB), 0b10100101100100101011000)

class TestLong(TestInteger):
	'''Test the models.integer.Long Model'''
	model = Long

	def setUp(self):
		'''Sets up the test cases'''
		self.testA = self.model(0b10100101L)
		self.testB = self.model(0b0100100101011000L)
		self.testC = self.model(0b10010110L)
