import os

import pandas as pd
import requests

from .CommonDataCollectionTasks import DataCollectionDefaults


class ApiPsuDataCollection(DataCollectionDefaults):

    def __init__(self):

        super(ApiPsuDataCollection, self).__init__()
        self.cols_psu_file = 'app/analytics_dir/famews_modules/input_files/psu_fields.txt'
        self.__psu_df = None

    @property
    def psu_df(self):
        """
        Working directory of analysis
        :return: directory
        """
        return self.__psu_df

    @psu_df.setter
    def psu_df(self, country):  # , filename_date_part, save_selected_api_records):
        """"
        Fill the dataframe for PSU data in the country and make it available to the whole class

        :param country: name of country
        :return: refresh a class cope dataframe
        """

        response_scouting = requests.get(self._PSU_SCOUT_SURVEY_JSON)

        try:
            records = response_scouting.json()
        except requests.exceptions.HTTPError as error:
            print(error)

        df_scouting = pd.DataFrame.from_records(records['data'])
        cols = [c for c in df_scouting.columns if c.lower()[-3:] != '_id']
        df_scouting = df_scouting[cols]

        with open(self.cols_psu_file , 'r') as file_handle_psu:
            cols_psu = eval(file_handle_psu.read())
        df_scouting = df_scouting[cols_psu]

        # Fields I rename from the API or Merging
        file_fields_psu = os.path.abspath(os.path.join(os.path.dirname(__file__) ,
                                                       'input_files/' ,
                                                       'psu_rename_fields.txt'))

        with open(file_fields_psu , 'r') as inf:
            dict_from_file = eval(inf.read())

        df_scouting = df_scouting.loc[df_scouting['country'] == country]

        # TODO: Problem with date format
        df_scouting['date_of_survey'] = df_scouting['date_of_survey'].str.replace('PM', '')
        df_scouting['date_of_survey'] = df_scouting['date_of_survey'].str.replace('AM', '')
        df_scouting['date_of_survey'] = df_scouting['date_of_survey'].str.replace(',', '')
        df_scouting.dropna(subset=['date_of_survey'])
        df_scouting['date_of_survey'] = pd.to_datetime(df_scouting['date_of_survey'])
        # format='%d/%m/%Y')

        nan_value = float("NaN")
        df_scouting.replace("", nan_value, inplace=True)
        df_scouting.dropna(subset=super()._COLUMNS_COORDINATES)
        df_scouting.dropna(subset=super()._COL_PLANTS_INFESTED)
        df_scouting.mask(df_scouting.eq('nan')).dropna(subset=super()._COL_PLANTS_INFESTED, inplace=True)
        df_scouting[super()._COLUMNS_COORDINATES].apply(pd.to_numeric)  # , errors='coerce')
        df_scouting[super()._COL_PLANTS_INFESTED].apply(pd.to_numeric, errors='coerce')
        df_scouting['origin'] = 'PSU'
        df_scouting['scoutingPlantsChecked'] = 50
        df_scouting['scoutingPlantsFAW'] = df_scouting['station1_faw'] + df_scouting['station2_faw'] + \
                                           df_scouting['station3_faw'] + df_scouting['station4_faw'] +  \
                                           df_scouting['station5_faw']
        # df_scouting.dropna(subset=['station1_faw', 'station2_faw', 'station3_faw', 'station4_faw', 'station5_faw'])
        df_scouting.drop(['station1_faw', 'station2_faw', 'station3_faw', 'station4_faw', 'station5_faw'], axis=1, inplace=True)

        file_fields_psu = os.path.abspath(os.path.join(os.path.dirname(__file__) ,
                                                       'input_files/' ,
                                                       'psu_rename_fields.txt'))

        with open(file_fields_psu , 'r') as inf:
            dict_from_file = eval(inf.read())
        df_scouting.rename(columns=dict_from_file , inplace=True)

        # df_scouting.to_csv("psu.csv")

        # df_control = df_scouting.control.apply(pd.Series)
        # df_scouting = pd.concat([df_scouting.drop(['control'], axis=1),
        #                          df_control], axis=1)
        #
        # df_natural_enemies = df_scouting.natural_enemies.apply(pd.Series)
        # df_scouting = pd.concat([df_scouting.drop(['natural_enemies'], axis=1),
        #                          df_natural_enemies], axis=1)

        self.__psu_df = df_scouting