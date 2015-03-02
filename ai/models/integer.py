# Rushy Panchal
# ai/models/integer.py

class IntegerBase:
	'''A wrapper base'''
	def __invert__(self):
		'''Invert the current value with the logical NOT operator'''
		value = self.real
		return self.dataType(value ^ (2**value.bit_length() - 1)) # use a XOR mask to flip the bits

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

	def moveBit(self, old, new, size = None):
		'''Move a bit from the "old" to "new" position'''
		value = self.real
		if old == new:
			return self.dataType(value)
		if not size:
			size = value.bit_length()
		value = (value | (1 << new)) & (((2**(size - old - 1) -1) << (old + 1)) | (2**old - 1))
		return self.dataType(value)

	def getBit(self, position):
		'''Get the bit in a certain position'''
		value = self.real

		return (value >> position) & (2**(value.bit_length() - position + 2) + 1)

	def concat(self, n, size = None):
		'''Concatenates two integers'''
		return self.dataType((self.real << (size if size else n.bit_length())) | n)

class Integer(IntegerBase, int):
	'''A wrapper around native ints that allows for various logical operators'''
	pass

class Long(IntegerBase, long):
	pass

IntegerBase.dataType = int
Integer.dataType = Integer
Long.dataType = Long