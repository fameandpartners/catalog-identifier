import pandas as pd
from flask import Blueprint
import re
import config
from flask_restplus import Resource, fields, reqparse, Namespace, Api
from flask.json import jsonify
from pymongo import MongoClient
missing_product_id = set()
client = MongoClient(config.MONGO_URI)
db_name = config.MONGO_DB_NAME

def match_catalog(raw_gui):
    #Split the parameter input and try to match attributes.
    parameter_list = raw_gui.split('~')
    temp_df = catalog_data
    temp_df['matches'] = temp_df['id_split'].apply(lambda x: match_attributes(x, parameter_list))
    first_item = temp_df.sort_values('matches').iloc[0]

    #If it doesnt match, log and return the original information
    if not first_item['matches']:
        client[db_name]['logs'].insert_one({
            'raw_gui': raw_gui,
            'matched_gui': raw_gui,
            'success': False
        })
        return {
            'matched_gui': raw_gui,
            'success': False
        }

    client[db_name]['logs'].insert_one({
        'raw_gui': raw_gui,
        'matched_gui': first_item['id'],
        'success': True
    })
    return {
        'matched_gui': first_item['id'],
        'success': True
    }

# Custom Studio Must Match: ID - Always the first element,
# Second and Third Position (but can flip), B+Number (Any), C+Number (Any)
def match_attributes(reference_list, parameter_list):
    if parameter_list[0] != reference_list[0]:
        return None
    #If it is custom studio, implement a more strict rule of matching
    if parameter_list[0] in ['FPG1003', 'FPG1002', 'FPG1001']:
        #Must match color
        color_match = False
        b_match_flag = False
        c_match_flag = False

        for c in parameter_list[1:3]:
            if c in reference_list[1:3]:
                color_match = True

        for param in parameter_list[1:]:
            #Must match one of the B + Number
            if re.match('B[0-9]+', param):
                if param in reference_list:
                    b_match_flag = True

            # Must match one of the C + Number
            if re.match('C[0-9]+', param):
                if param in reference_list:
                    c_match_flag = True

        if not color_match or not b_match_flag or not c_match_flag:
            return None

    #compute the matching score
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
        return jsonify(match_catalog(args['raw_gui']))


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