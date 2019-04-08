import pandas as pd
from flask import Blueprint
from flask_restplus import Resource, fields, reqparse, Namespace, Api
from flask.json import jsonify
missing_product_id = set()

def match_catalog(raw_gui):
    parameter_list = raw_gui.split('~')
    temp_df = catalog_data
    temp_df['matches'] = temp_df['id_split'].apply(lambda x: match_attributes(x, parameter_list))
    first_item = temp_df.sort_values('matches').iloc[0]
    if not first_item['matches']:
        missing_product_id.add(parameter_list[0])
        return raw_gui
    return first_item['id']

def match_attributes(reference_list, parameter_list):
    if parameter_list[0] != reference_list[0]:
        return None
    else:
        score = 0
        for param in reference_list:
                if param in parameter_list:
                    score += 1
        return score

url = 'http://api.godatafeed.com/v1/9bdeb5a1a7e5404f92b3133261a797e9/feeds/RE1pNHgyTnVDNm9sc3VPcUZVd1d1Zz09/download'
catalog_data = pd.read_csv(url)
catalog_data['id_split'] = catalog_data['id'].apply(lambda x: x.split('~'))


catalog_matching_input = reqparse.RequestParser()
catalog_matching_input.add_argument('raw_gui', required=True, type=str,
                                                 help='Raw GUI Input')

class CatalogMatching(Resource):
    def get(self):
        args = catalog_matching_input.parse_args()
        return jsonify({
            'matched_gui': match_catalog(args['raw_gui'])
        })


# testing = pd.read_csv('unmatched.csv')
# matching_result = []
# for index, row in testing.iterrows():
#     matched = match_catalog(row['Content ID'])
#     matching_result.append({
#         'original': row['Content ID'],
#         'matched': matched
#     })
#
# pd.DataFrame(matching_result).to_csv('matching_result.csv')

# print(missing_product_id)