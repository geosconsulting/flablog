import requests
import pandas as pd

from .famews import FAMEWSApi

class ManageFAMEWSApiPSU(FAMEWSApi):

    def __init__(self):
        super(ManageFAMEWSApiPSU, self).__init__()


    def get_scoutings(self):

        response = requests.get(self.url_psu_scoutings)
        try:
            records = response.json()
        except ValueError as e:
            print(e)

        df = pd.DataFrame.from_records(records['data'])

        columns_drop = [col for col in df.columns if '_id' in col]
        columns_drop.append('control')
        columns_drop.append('survey_scout_data')

        df.drop(columns_drop, axis=1, inplace=True)
        df.replace(to_replace=[None], value=0, inplace=True)

        return df


    def get_traps(self):

        response = requests.get(self.url_psu_traps)
        try:
            records = response.json()
        except ValueError as e:
            print(e)

        df = pd.DataFrame.from_records(records['data'])

        return df



