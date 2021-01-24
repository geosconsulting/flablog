"""
Collecting data from CIO API
"""
import os
import warnings

import pandas as pd
import requests

from .CommonDataCollectionTasks import DataCollectionDefaults

warnings.filterwarnings('ignore')


class ApiCioDataCollection(DataCollectionDefaults):

    """
    CIO API can be subselected by country, starting date and ending date

    :country str
    :min_date str
    :max_date str
    """

    def __init__(self , num_rec=250000 , min_date='2018-01-01' , max_date='2021-12-31'):

        super(ApiCioDataCollection , self).__init__()

        self.__num_rec = num_rec
        self.__min_date = min_date
        self.__max_date = max_date
        self.__cols_cio_file = 'app/analytics/famews_modules/input_files/cio_fields.txt'
        self.__cio_df = None

    def __str__(self):
        return '{} {} {}'.format(self.__num_rec, self.__min_date, self.__max_date)

    def __repr__(self):
        return '<ApiCioDataCollection object ({} {} {})>'.format(self.__num_rec,
                                                                 self.__min_date,
                                                                 self.__max_date)

    @property
    def num_rec(self):
        """
        How many records will be fetched
        :return: number of records
        """
        return self.__num_rec

    @num_rec.setter
    def num_rec(self, num_rec):
        """
        Set the number of records that will be fetched
        :param num_rec: integer number of records
        :return: nothing
        """
        self.__num_rec = num_rec

    @property
    def min_date(self):
        return self.__min_date

    @min_date.setter
    def min_date(self, min_date):
        self.__min_date = min_date

    @property
    def max_date(self):
        return self.__max_date

    @max_date.setter
    def max_date(self, max_date):
        self.__max_date = max_date

    @property
    def cio_df(self):
        """
        Working directory of analysis
        :return: directory
        """
        return self.__cio_df

    @cio_df.setter
    def cio_df(self, iso2):  # , filename_date_part, save_selected_api_records):
        """
        Fill the dataframe for PSU data in the country and make it available to the whole class
        :param iso2: iso2 of country
        :return: create a class scope dataframe
        """

        if DataCollectionDefaults.country_name != 'All' and DataCollectionDefaults.country_name != 'all':
            params = {'limit': self.num_rec,
                      'data.country': iso2,
                      'data.date__gte': self.min_date,
                      'data.date__lte': self.max_date}
        else:
            params = {'limit': self.num_rec,
                      'data.date__gte': self.min_date,
                      'data.date__lte': self.max_date}

        response = requests.get(self._CIO_FAMEWS_SUBMISSION, params=params)

        file_fields_cio = os.path.abspath(os.path.join(os.path.dirname(__file__) ,
                                                       'input_files/' ,
                                                       'cio_rename_fields.txt'))
        try:
            records = response.json()
        except ValueError as error_collecting_json:
            print(error_collecting_json)

        df_records = pd.DataFrame.from_records(records)

        if df_records.empty:
            with open(file_fields_cio, 'r') as inf:
                dict_from_file = eval(inf.read())

            with open(self.__cols_cio_file , 'r') as file_handle_cio:
                cols_cio = eval(file_handle_cio.read())
            self.__cio_df = pd.DataFrame(columns=cols_cio)

        else:
            df_data_external = df_records[['_id', 'created', 'modified']]
            df_data = df_records['data']
            df_data_submission = df_data.apply(pd.Series)
            df_data_submission = pd.concat([df_data_external , df_data_submission] , axis=1)

            # Fields I retain from the API
            with open(self.__cols_cio_file , 'r') as file_handle_cio:
                cols_cio = eval(file_handle_cio.read())

            # Fields I rename from the API or Merging
            file_fields_cio = os.path.abspath(os.path.join(os.path.dirname(__file__) ,
                                                           'input_files/' ,
                                                           'cio_rename_fields.txt'))

            with open(file_fields_cio , 'r') as inf:
                dict_from_file = eval(inf.read())

            df_data_submission = df_data_submission[cols_cio]

            # df_data_collected = df_data_submission.dataCollected.apply(pd.Series)
            # df_data_submission = pd.concat([df_data_submission.drop(['dataCollected'], axis=1),
            #                                 df_data_collected], axis=1)
            # df_natural_enemies = df_data_submission.fawNaturalEnemies.apply(pd.Series)
            # df_data_submission = pd.concat([df_data_submission.drop(['fawNaturalEnemies'], axis=1),
            #                                 df_natural_enemies], axis=1)
            # df_control_undertaken = df_data_submission.fawControlUndertaken.apply(pd.Series)
            # df_data_submission = pd.concat([df_data_submission.drop(['fawControlUndertaken'], axis=1),
            #                                 df_control_undertaken], axis=1)

            df_data_submission['date'] = df_data_submission['date'].astype('datetime64[ns]')
            df_data_submission.rename(columns=dict_from_file, inplace=True)
            # df_data_submission.dropna(subset=super()._COL_PLANTS_INFESTED)
            # df_data_submission[super()._COL_PLANTS_INFESTED].apply(pd.to_numeric)  # , errors='coerce')
            df_data_submission['country'] = super().country_name
            df_data_submission['origin'] = 'CIO'

            # df_data_submission.to_csv("cio.csv")

            self.__cio_df = df_data_submission
