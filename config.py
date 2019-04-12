import os

#Flask Settings
DEBUG = True
PORT = os.environ.get('PORT', 7000)
HOST = os.environ.get('HOST', "0.0.0.0")

#Mongodb Setting
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://fnp:fnpadmin1@ds163764.mlab.com:63764/heroku_l189wfkq')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'heroku_l189wfkq')