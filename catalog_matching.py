from pymongo import MongoClient
import pandas as pd
import re
import config
from datetime import datetime, timedelta
import dateutil.parser

client = MongoClient(config.MONGO_URI)
db_name = config.MONGO_DB_NAME
url = config.CATALOG_URL

def get_file_or_use_existing():
    """
    Check if the csv file is updated within the past 12 hours, if it is not, update it with a new file

    """

    file = open('last_updated', 'r')
    lines = file.readlines()
    if (lines == []):
        last_updated_time = datetime.now() - timedelta(hours=14)
    else:
        last_updated_time = dateutil.parser.parse(lines[0])

    if last_updated_time < (datetime.now() - timedelta(hours=12)):
        file = open('last_updated', 'w')

        print('Getting New Catalog Data')
        pd.read_csv(url).to_csv('catalog.csv')
        file.writelines([datetime.now().isoformat()])
        return pd.read_csv('catalog.csv')
    else:
        return pd.read_csv('catalog.csv')


def match_catalog(raw_gui):
    """
    Mathces the product catalog given a raw GUI from F&P's website

    Attributes:
        @:param raw_gui : string, raw GUI string from spree ecommerce

    Returns:
        Dict: {
            'matched_gui': the gui matched from the system
            'success': status of the matching operation
        }

    """
    # TODO: make the url a parameter, instead of hard coded. But right now there is no point for this.
    catalog_data = get_file_or_use_existing()
    catalog_data['id_split'] = catalog_data['id'].apply(lambda x: x.split('~'))

    # Split the parameter input and try to match attributes
    parameter_list = raw_gui.split('~')
    temp_df = catalog_data
    temp_df['matches'] = temp_df['id_split'].apply(lambda x: match_attributes(x, parameter_list))
    first_item = temp_df.sort_values('matches').iloc[0]

    # If it doesnt match, log and return the original information
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

    #Log the result to the logging db
    client[db_name]['logs'].insert_one({
        'raw_gui': raw_gui,
        'matched_gui': first_item['id'],
        'success': True
    })

    # If a match is found, return the newly matched information
    return {
        'matched_gui': first_item['id'],
        'success': True
    }


# Custom Studio Must Match: ID - Always the first element,
# Second and Third Position (but can flip), B+Number (Any), C+Number (Any)
def match_attributes(reference_list, parameter_list):
    """
    Match attributes of the split gui with the split gui of a product in the Facebook Catalog

    Attributes:
        @:param reference_list : [string], GUI string split by '~' from the Facebook Catalog
        @:param parameter_list : [string], GUI string split by '~' from the GUI input

    Returns:
        int : the matching score of the parameter list against the reference list, return None if no match can be made

    """
    if parameter_list[0] != reference_list[0]:
        return None

    # If it is custom studio, implement a more strict rule of matching
    if parameter_list[0] in ['FPG1003', 'FPG1002', 'FPG1001']:
        # Must match color
        color_match = False
        b_match_flag = False
        c_match_flag = False

        for c in parameter_list[1:3]:
            if c in reference_list[1:3]:
                color_match = True

        for param in parameter_list[1:]:
            # Must match one of the B + Number
            if re.match('B[0-9]+', param):
                if param in reference_list:
                    b_match_flag = True

            # Must match one of the C + Number
            if re.match('C[0-9]+', param):
                if param in reference_list:
                    c_match_flag = True

        if not color_match or not b_match_flag or not c_match_flag:
            return None

    # Compute the matching score
    score = 0
    for param in reference_list:
        if param in parameter_list:
            score += 1
    return score
