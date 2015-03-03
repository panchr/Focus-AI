# Rushy Panchal
# ai/config.py

from numpy import uint32

# Global configuration options
ENV = "development" # development mode
DEV_MODE = (ENV == "development")

HOST = "localhost"
PORT = 27017

# AI Settings
RULE_MATCHES = 3
WEIGHT_DELTA = 1

STORAGE_DATATYPE = uint32
NORMALIZE_THRESHOLD = 2**31 - 2
NORMALIZE_THRESHOLD_NEG = -1 * NORMALIZE_THRESHOLD
