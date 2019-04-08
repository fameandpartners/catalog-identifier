import os

#Flask Settings
DEBUG = True
PORT = os.environ.get('PORT', 7000)
HOST = os.environ.get('HOST', "0.0.0.0")