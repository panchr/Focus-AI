# Rushy Panchal
# tests/__init__.py

import os.path
import sys

def setup():
	'''Set up the test package'''
	sys.path.append(os.path.join(os.path.abspath("."), "tests"))
