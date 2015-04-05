# Rushy Panchal
# ai/config.py

from numpy import int32, float32

# Global configuration options
ENV = "development" # development mode
DEV_MODE = (ENV == "development")

APP_HOST = "127.0.0.1"
APP_PORT = 7337

DB_HOST = "localhost"
DB_PORT = 27017
DB_NAME = "senior_focus"

# AI Settings
RULE_MATCHES = 3
WEIGHT_DELTA = 1

STORAGE_DATATYPE = int32
NORMALIZE_THRESHOLD = 2**31 - 2
NORMALIZE_THRESHOLD_NEG = -1 * NORMALIZE_THRESHOLD
