from flask import Flask
from flask_restplus import Api
from flask_cors import CORS
from api import CatalogMatching
import pytz

class Application(object):

    def __init__(self, config, debug=True):
        self.flask_app = Flask(__name__)
        CORS(self.flask_app)
        api = Api(self.flask_app)
        api.add_resource(CatalogMatching, '/match_catalog')

        self.debug = debug
        self._configure_app(config)

    def _configure_app(self, env):
        self.flask_app.config.from_object('config')

    def start_app(self):
        self.flask_app.config['HOST'] = '0.0.0.0'
        self.flask_app.run(host=self.flask_app.config['HOST'], port=int(self.flask_app.config['PORT']), debug=self.debug)
