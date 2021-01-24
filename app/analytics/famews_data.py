import os
from sqlalchemy import create_engine
import pandas as pd

import app
from .famews_modules import ApisDataMerge as scouting

working_dir = os.path.dirname(os.path.realpath(__file__))
api_obj = scouting.ApiMergeDataCollection()

def write_data(country_code):

    if country_code != 'None':
        api_obj.country_iso = country_code
        api_obj.country_name = country_code
    print("Fetching {} - {}".format(country_code , api_obj.country_name))

    # Collecting CIO data
    try:
        api_obj.cio_df = country_code
        api_obj.min_date = '2018-01-10'
        print("{} entries found for {} in CIO API".format(len(api_obj.cio_df), api_obj.country_name))
    except ValueError as e:
        print(e)

    # Collecting PSU data
    try:
        api_obj.psu_df = api_obj.country_name
        print("{} entries found for {} in PSU API".format(len(api_obj.psu_df) , api_obj.country_name))
    except ValueError as e:
        print(e)

    # Combining CIO & PSU data
    try:
        all_records = api_obj.combined_df()
    except ValueError as data_merge_error:
       print("Data Merge fails for {}".format(data_merge_error))

    api_obj.write_2_sqlite(all_records)


def get_data(country_code):

    engine = create_engine(app.config.Config.SQLALCHEMY_DATABASE_URI)
    con = engine.connect()

    df_all = pd.read_sql_table(con=con , table_name=country_code.lower())

    return(df_all)
