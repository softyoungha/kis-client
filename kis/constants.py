import os


# constants
KIS_HOME = os.getenv("KIS_HOME", os.getcwd())
LIB_PATH = os.path.realpath(os.path.dirname(__file__))

# parse env
KIS_APP_KEY = os.getenv("KIS_APP_KEY", "")
KIS_APP_SECRET = os.getenv("KIS_APP_SECRET", "")
KIS_ACCOUNT = os.getenv("KIS_ACCOUNT", "")
