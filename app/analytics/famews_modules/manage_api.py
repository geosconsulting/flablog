import requests
import pandas as pd
# OBSOLETE REMOVED
# from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

# REPLACEMENT MATPLOTLIB
# import cartopy.crs as ccrs

import sys

from famews import FAMEWSApi


class ManageFAMEWSApi(FAMEWSApi):

    def __init__(self):
        
        super(ManageFAMEWSApi, self).__init__()

        self._num_rec = 250000
        self._country = 'all'
        self._min_date = '2018-01-01'
        self._max_date = '2020-12-31'

    @property
    def num_rec(self):
        """
        How many records will be fetched
        :return: number of records
        """
        return self._num_rec

    @num_rec.setter
    def num_rec(self, num_rec):
        """
        Set the number of records that will be fetched
        :param num_rec: integer number of records
        :return: nothing
        """
        self._num_rec = num_rec

    @property
    def country(self):
        """
        The country for which the data will be selected
        :return:
        """
        return self._country

    @country.setter
    def country(self, cntry):
        """
        Set the country for selecting the records for
        :param cntry: ISO2
        :return: Nothing
        """
        self._country = cntry

    @property
    def min_date(self):
        return self._min_date

    @min_date.setter
    def min_date(self, min_date):
        self._min_date = min_date

    @property
    def max_date(self):
        return self._max_date

    @max_date.setter
    def max_date(self, max_date):
        self._max_date = max_date

    def get_records_from_api(self, filename_date_part, save_selected_api_records):
        """

        :param filename_date_part:
        :param save_selected_api_records:
        :return:
        """

        if self.country != 'All' and self.country != 'all':
            params = {'limit': self._num_rec,
                      'data.country': self._country,
                      'data.date__gte': self._min_date,
                      'data.date__lte': self._max_date}
        else:
            params = {'limit': self._num_rec,
                      'data.date__gte': self._min_date,
                      'data.date__lte': self._max_date}

        response = requests.get(self.url, params=params)

        try:
            records = response.json()
        except ValueError as e:
            print(e)
            pass


        df = pd.DataFrame.from_records(records)

        if df.empty:
            print("No records available for {} between {} and {}".format(self._country,
                                                                         self._min_date,
                                                                         self._max_date))
            # quit()
            sys.exit(1)
        else:
            df_data_external = df[['_id', 'created', 'modified']]
            df_data = df['data']
            df_data_submission = df_data.apply(pd.Series)
            df_data_id = pd.concat([df_data_external, df_data_submission], axis=1)

        file_created = False
        if save_selected_api_records:
            df_data_id_filename = 'output_apis/' + self._country + "_" + filename_date_part + '.csv'
            try:
                df_data_id.to_csv(df_data_id_filename, encoding='utf8')
                file_created = True
            except IOError:
                file_created = False

        return records, df, df_data_id, file_created

    def delete_single_record_by_id(self, root_id, permission):
        """
            To be completed
        :param root_id: id of the record to be deleted
        :param permission: if true the record is actually deleted otherwise is just checked
        :return:
        """
        transaction_outcome = False
        try:
            url_delete = self.url + root_id
            if permission == 'erase':
                print("I am deleting!!!!!!!")
                requests.delete(url_delete, headers=self.headers)
                transaction_outcome = True
        except IOError as e:
            print(e)
            transaction_outcome = False

        return transaction_outcome

    def remove_scouting_traps_errors(self, ids, permission):

        counting_records = 0
        for id_current in ids:
            url_delete = self.url + id_current
            if permission == 'erase':
                requests.delete(url_delete, headers=self.headers)
                print("Deleted {}".format(url_delete))
            counting_records += 1

        return " {} records to be deleted".format(counting_records)

    @staticmethod
    def modify_lat_lon_scouting_traps_errors(**kwargs):

        counts_records = 0

        for key, value in kwargs.iteritems():
            print(key, value)

            counts_records += 1

        return " {} records modified".format(counts_records)

    @staticmethod
    def collect_coords_to_be_mapped(df):

        ids = df['_id'].tolist()
        lats = df['latitude'].tolist()
        lons = df['longitude'].tolist()

        return lats, lons, ids


    #TODO: Replace with GeoViews or Cartpy
    @staticmethod
    def mapping_scoutings(list_of_latitudes , list_of_longitudes , lat_0_p , lon_0_p ,
                          lower_left_corner_longitude , lower_left_corner_latitude ,
                          upper_right_corner_longitudes , upper_right_corner_latitudes ,
                          cntry , msg):
        pass

        # m = Basemap(resolution='i' ,  # c, l, i, h, f or None. crude, low, intermediate, high or full.
        #             projection='merc' ,
        #             lat_0=lat_0_p ,
        #             lon_0=lon_0_p ,
        #             llcrnrlon=lower_left_corner_longitude ,
        #             llcrnrlat=lower_left_corner_latitude ,
        #             urcrnrlon=upper_right_corner_longitudes ,
        #             urcrnrlat=upper_right_corner_latitudes ,
        #             area_thresh=10000
        #             )
        #
        # m.drawcoastlines()
        # m.drawcountries()
        # m.drawstates()
        # m.drawparallels(range(-90, 90, 10))
        # m.drawmeridians(range(-180, 180, 10))
        # m.drawmapboundary(fill_color='#46bcec')
        # m.fillcontinents(color='white', lake_color='#46bcec')
        #
        # x, y = m(list_of_longitudes , list_of_latitudes)
        #
        # m.scatter(x, y, marker='o', color='r', zorder=5)
        # plt.title("Survey Locations for " + cntry + " - " + msg)
        #
        # plt.show()
