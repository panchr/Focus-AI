// Rushy Panchal
// ai/ext/integer.c
// Provides bitstring operations in C

#include <math.h>

unsigned int countBits(unsigned int n);
unsigned int not(unsigned int n);
unsigned int rcirc(unsigned int x, unsigned int n);
unsigned int lcirc(unsigned int x, unsigned int n);

int main(void) {
	// Main process
	return 0;
	}

unsigned int countBits(unsigned int n) {
	// Counts the number of bits in n
	unsigned int count;
	while (n > 0) {
		count++;
		n = n >> 1;
		}
	return count;
	}

unsigned int not(unsigned int n) {
	// Calculate the logical NOT of n
	unsigned int x = ~n & (unsigned int) (pow(2, countBits(n)) - 1);
	return x;
	}

unsigned int rcirc(unsigned int x, unsigned int n) {
	// Calculate the RCIRC of a bitstring
	unsigned int numBits = countBits(x);
	n = n % numBits;
	if (n == numBits) {
		return x;
		}

	unsigned int toShift = numBits - n;
	unsigned int right = x >> n;
	unsigned int left = (x << toShift) ^ (right << numBits);
	return left | right;
	}

unsigned int lcirc(unsigned int x, unsigned int n) {
	// Calculate the LCIRC of a bitstring
	unsigned int numBits = countBits(x);
	n = n % numBits;
	if (n == numBits) {
		return x;
		}

	unsigned int toShift = numBits - n;
	unsigned int right = x >> toShift;
	unsigned int left = (x << n) ^ (right << numBits);
	return left | right;
	}
