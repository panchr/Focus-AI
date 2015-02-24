# Rushy Panchal
# ai/models/bitstringpy

from models.model import CustomTypeBase

class Integer(int):
	'''A wrapper around native ints that allows for various logical operators'''
	def __invert__(self):
		'''Invert the current value with the logical NOT operator'''
		value = self.real
		return ~value & (2**value.bit_length() - 1)

	def rcirc(self, n):
		'''RCIRC the bitstring n times'''
		value = self.real
		numBits = value.bit_length()
		n = n % numBits # make sure n is within the range of (0, numBits) inclusive
		if (n == numBits): # RCIRC(x, n) for n = (number of bits in x) is equal to x
			return value

		toShift = numBits - n
		right = value >> n # remove the last n bits
		left = (value << toShift) ^ (right << numBits) # get the first "toShift" bits
		return left | right # combine the left and right halves

	def lcirc(self, n):
		'''LCIRC the bitstring n times'''
		value = self.real
		numBits = value.bit_length()
		n = n % numBits # make sure n is within the range of (0, numBits) inclusive
		if (n == numBits): # LCIRC(x, n) for n = (number of bits in x) is equal to x
			return value

		toShift = numBits - n
		right = value >> toShift # remove the last "toShift" bits
		left = (value << n) ^ (right << numBits) # get the first n bits
		return left | right # combine the left and right halves

class Bitstring(CustomTypeBase):
	'''A Custom Type representing a bit string'''
	mongo_type = int
	python_type = Integer
	init_type = int

	def to_bson(self, bitstring):
		'''Converts the Integer to a native int'''
		return bitstring.real

	def to_python(self, value):
		'''Converts a native int to an Integer'''
		return Integer(value)
