from app import Application
import os
from flask_restplus import Resource, reqparse, Api
from flask.json import jsonify
from catalog_matching import *

app = Application(os.environ, debug=True)
api = Api(app.flask_app)

catalog_matching_input = reqparse.RequestParser()
catalog_matching_input.add_argument('raw_gui', required=True, type=str,
                                                 help='Raw GUI Input')


@api.expect(catalog_matching_input)
@api.route('/match-catalog')
class CatalogMatching(Resource):
    def get(self):
        args = catalog_matching_input.parse_args()
        return jsonify(match_catalog(args['raw_gui']))