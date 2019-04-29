import os

#Flask Settings
DEBUG = True
PORT = os.environ.get('PORT', 7000)
HOST = os.environ.get('HOST', "0.0.0.0")

#Mongodb Setting
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://fnp:fnpadmin1@ds163764.mlab.com:63764/heroku_l189wfkq')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'heroku_l189wfkq')

CATALOG_URL = os.environ.get('CATALOG_URL',
        'http://api.godatafeed.com/v1/9bdeb5a1a7e5404f92b3133261a797e9/feeds/RE1pNHgyTnVDNm9sc3VPcUZVd1d1Zz09/download')