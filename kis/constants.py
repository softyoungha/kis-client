import os

# constants
KIS_HOME = os.getenv("KIS_HOME", os.getcwd())
LIB_PATH = os.path.realpath(os.path.dirname(__file__))
