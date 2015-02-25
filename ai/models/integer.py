# Rushy Panchal
# ai/models/integer.py

class IntegerBase:
	'''A wrapper base'''
	def __invert__(self):
		'''Invert the current value with the logical NOT operator'''
		value = self.real
		return self.dataType(~value & (2**value.bit_length() - 1))

	def rcirc(self, n):
		'''RCIRC the bitstring n times'''
		value = self.real
		numBits = value.bit_length()
		n = n % numBits # make sure n is within the range of (0, numBits) inclusive
		if (n == numBits): # RCIRC(x, n) for n = (number of bits in x) is equal to x
			return self.dataType(value)

		toShift = numBits - n
		right = value >> n # remove the last n bits
		left = (value << toShift) ^ (right << numBits) # get the first "toShift" bits
		return self.dataType(left | right) # combine the left and right halves

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
		return self.dataType(left | right) # combine the left and right halves

	def concat(self, n):
		'''Concatenates two integers'''
		return self.dataType((self.real << n.bit_length()) | n)

class Integer(IntegerBase, int):
	'''A wrapper around native ints that allows for various logical operators'''
	pass

class Long(IntegerBase, long):
	pass

IntegerBase.dataType = int
Integer.dataType = Integer
Long.dataType = Long