import datetime
import ee
from ee.batch import Export
import eeconvert
from famews import FAMEWSApi
import datetime
import pandas as pd
import geopandas as gpd
from geoalchemy2 import Geometry, WKTElement
from sqlalchemy import *
from sqlalchemy import exc
from itertools import cycle
import matplotlib.pyplot as plt

class ManageFAMEWSGEE(FAMEWSApi):

    def __init__(self):
        super(ManageFAMEWSGEE, self).__init__()
        ee.Initialize()

        self.__chirps_collection = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
        # self.chirps_collection = ee.ImageCollection('UCSB-CHG/CHIRPS/PENTAD')
        self.__era5_collection = ee.ImageCollection('ECMWF/ERA5/DAILY')

        # Creating SQLAlchemy's engine to use
        self.engine = create_engine('postgresql://postgres:antarone@localhost:5432/famews')


    def clean_submission_data(self,df_points_scoutings):

        df_cio_keep = [u'_id', u'date', u'latitude', u'longitude', u'scoutingPercentageFAW']
        df_cio_gee = df_points_scoutings.loc[:, df_cio_keep]

        df_cio_gee["latitude"] = pd.to_numeric(df_cio_gee["latitude"])
        df_cio_gee["longitude"] = pd.to_numeric(df_cio_gee["longitude"])
        df_cio_gee['date'] = pd.to_datetime(df_cio_gee['date'])
        df_cio_gee['date'] = [d.date() for d in df_cio_gee['date']]
        df_cio_gee.dropna(subset=['scoutingPercentageFAW'], inplace=True)
        df_cio_gee['scoutingPercentageFAW'] = df_cio_gee['scoutingPercentageFAW']
        df_cio_gee.rename(columns={"scoutingPercentageFAW": "prevalence"}, inplace=True) #"_id":"id",
        # df_cio_gee.set_index("id", inplace=True)
        df_cio_gee_noDuplicates = df_cio_gee.drop_duplicates(subset=['date', 'latitude', 'longitude'], keep='last')
        list_of_dates = pd.Series(df_cio_gee_noDuplicates.date.unique())

        return df_cio_gee_noDuplicates, list_of_dates

    def API_export_PGIS(self, country, gdf_API_data):

        df_cio_keep_noGeo = ["_id", "date", "country", "cropFertilizer", "cropFieldSize", "cropFieldSizeUnit",
                             "cropHealth", "cropIrrigation", "cropMain", "cropPlantingDate", "cropStage", "cropVariety",
                             "date", "fawCropDamage", "fawCurrentDamage", "fawDeadLarvae", "fawPreviousDamage",
                             "latitude", "longitude", "rainLastDate", "region", "scoutingPercentageFAW",
                             "scoutingPlantsChecked", "scoutingPlantsFAW",  "cropRotation", "rainAmount"]

        df_cio = gdf_API_data.loc[:, df_cio_keep_noGeo]

        table_name_API_data = "data_" + country.lower()
        df_cio.to_sql(table_name_API_data,
                            self.engine,
                            if_exists='replace',
                            index=False)

        return table_name_API_data

    def calculate_timeframe_of_scoutings(self, scouting_date):

        scouting_datetime = datetime.datetime.combine(scouting_date, datetime.datetime.min.time())

        dd = datetime.timedelta(days=21)
        analysis_initial_date = scouting_datetime - dd

        return analysis_initial_date , scouting_datetime

    def get_CHIRPS_dates(self):

        # Get the date range of images in the collection.
        rango = self.__chirps_collection.reduceColumns(ee.Reducer.minMax(), ["system:time_start"])

        # Passing numeric date to standard
        init_date = ee.Date(rango.get('min')).getInfo()['value'] / 1000.
        init_date_f = datetime.datetime.utcfromtimestamp(init_date).strftime('%Y-%m-%d %H:%M:%S')

        last_date = ee.Date(rango.get('max')).getInfo()['value'] / 1000.
        last_date_f = datetime.datetime.utcfromtimestamp(last_date).strftime('%Y-%m-%d %H:%M:%S')

        date_for_table = last_date_f.split(" ")[0]

        return init_date_f,last_date_f,date_for_table

    def get_ERA5_dates(self):

        # Get the date range of images in the collection.
        rango = self.__era5_collection.reduceColumns(ee.Reducer.minMax(), ["system:time_start"])

        # Passing numeric date to standard
        init_date = ee.Date(rango.get('min')).getInfo()['value'] / 1000.
        init_date_f = datetime.datetime.utcfromtimestamp(init_date).strftime('%Y-%m-%d %H:%M:%S')

        last_date = ee.Date(rango.get('max')).getInfo()['value'] / 1000.
        last_date_f = datetime.datetime.utcfromtimestamp(last_date).strftime('%Y-%m-%d %H:%M:%S')

        date_for_table = last_date_f.split(" ")[0]

        return init_date_f,last_date_f,date_for_table

    def subset_dataframe_scoutings_CHIRPS_availabilty(self,df_cio_gee_noDuplicates,last_date_f):

        upper_date_threshold = datetime.datetime.strptime(last_date_f, '%Y-%m-%d %H:%M:%S')
        mask_upToLastCHIRPS = (df_cio_gee_noDuplicates['date'] <= upper_date_threshold.date())
        df_upToLastCHIRPS = df_cio_gee_noDuplicates.loc[mask_upToLastCHIRPS]

        list_of_dates = pd.Series(df_upToLastCHIRPS.date.unique())

        return df_upToLastCHIRPS,list_of_dates

    def subset_dataframe_scoutings_ERA5_availabilty(self,df_cio_gee_noDuplicates,last_date_f):

        upper_date_threshold = datetime.datetime.strptime(last_date_f, '%Y-%m-%d %H:%M:%S')
        mask_upToLastERA5 = (df_cio_gee_noDuplicates['date'] <= upper_date_threshold.date())
        df_upToLastERA5 = df_cio_gee_noDuplicates.loc[mask_upToLastERA5]

        list_of_dates = pd.Series(df_upToLastERA5.date.unique())

        return df_upToLastERA5,list_of_dates

    def gee_CHIRPS_filtering_by_date(self, analysis_initial_datetime, analysis_final_datetime):

        chirps_filtered = self.__chirps_collection.filterDate(analysis_initial_datetime,
                                                              analysis_final_datetime).select('precipitation')

        num_chirps = chirps_filtered.size().getInfo()

        return chirps_filtered,num_chirps

    def gee_ERA5_filtering_by_date(self, analysis_initial_datetime, analysis_final_datetime):

        era5_filtered = self.__era5_collection.filterDate(analysis_initial_datetime,
                                                          analysis_final_datetime).select('mean_2m_air_temperature')

        num_era5 = era5_filtered.size().getInfo()

        return era5_filtered, num_era5

    def split_points_by_day(self,all_submissions,submission_date):

        mask = (all_submissions['date'] == submission_date)
        df_oneDay = all_submissions.loc[mask]
        gdf_oneDay = gpd.GeoDataFrame(df_oneDay, geometry=gpd.points_from_xy(df_oneDay.longitude, df_oneDay.latitude))
        gdf_oneDay.drop([u'latitude', u'longitude'], axis=1, inplace=True)

        return gdf_oneDay

    def extracting_precipitation_for_scoutings(self, gdf_daily_points, chirps_selected):

        gdf_oneDay_noDate = gdf_daily_points.drop(['date'], axis=1)
        daily_points_gee = eeconvert.gdfToFc(gdf_oneDay_noDate)

        def fill(img, ini):

          # type cast
          initial_features = ee.FeatureCollection(ini)

          # gets the values for the points in the current img
          points_with_precipitation = img.reduceRegions(collection= daily_points_gee,
                                                        reducer = ee.Reducer.first(),
                                                        scale = 10) #.get("precipitation")

          # gets the date of the img
          date = img.date().format()

          #writes the date in each feature
          points_with_date_addedd = points_with_precipitation.map(lambda f: f.set("date", date))

          # merges the FeatureCollections
          return initial_features.merge(points_with_date_addedd)

        # Empty Collection to fill
        ft = ee.FeatureCollection(ee.List([]))

        # Iterates over the ImageCollection
        ft_with_precipitation = ee.FeatureCollection(chirps_selected.iterate(fill, ft))

        gdf_precipitation = eeconvert.fcToGdf(ft_with_precipitation)
        gdf_precipitation.rename(columns={"first": "mm_rain","_id":"id_gee","date":"date_gee"},inplace=True)

        gdf_precipitation['geom'] = gdf_precipitation['geometry'].apply(lambda x: WKTElement(x.wkt, srid=4326))
        gdf_precipitation.drop(['geometry'], 1, inplace=True)

        return gdf_precipitation

    def extracting_temperature_for_scoutings(self, gdf_daily_points, era5_selected):

        gdf_oneDay_noDate = gdf_daily_points.drop(['date'], axis=1)
        daily_points_gee = eeconvert.gdfToFc(gdf_oneDay_noDate)

        def fill(img, ini):

          # type cast
          initial_features = ee.FeatureCollection(ini)

          # gets the values for the points in the current img
          points_with_temperature = img.reduceRegions(collection= daily_points_gee,
                                                        reducer = ee.Reducer.first(),
                                                        scale = 10) #.get("precipitation")

          # gets the date of the img
          date = img.date().format()

          #writes the date in each feature
          points_with_date_addedd = points_with_temperature.map(lambda f: f.set("date", date))

          # merges the FeatureCollections
          return initial_features.merge(points_with_date_addedd)

        # Empty Collection to fill
        ft = ee.FeatureCollection(ee.List([]))

        # Iterates over the ImageCollection
        ft_with_temperature = ee.FeatureCollection(era5_selected.iterate(fill, ft))

        gdf_temperature = eeconvert.fcToGdf(ft_with_temperature)
        gdf_temperature.rename(columns={"first": "temp_k","_id":"id_gee","date":"date_gee"},inplace=True)

        gdf_temperature['geom'] = gdf_temperature['geometry'].apply(lambda x: WKTElement(x.wkt, srid=4326))
        gdf_temperature.drop(['geometry'], 1, inplace=True)

        return gdf_temperature

    def data_export_PGIS_precipitation(self, country, gdf_precipitation_looping): #date_for_table,

        table_name_looping = "precipitation_" + country.lower() #+ "_before-" + date_for_table
        gdf_precipitation_looping.to_sql(table_name_looping,
                                         self.engine,
                                         if_exists='append',
                                         index=False,
                                         dtype={'geom': Geometry('POINT', srid='4326')})

        return table_name_looping


    def data_export_PGIS_temperature(self, country, gdf_precipitation_looping): #date_for_table,

        table_name_looping = "temperature_" + country.lower() #+ "_before-" + date_for_table
        gdf_precipitation_looping.to_sql(table_name_looping,
                                         self.engine,
                                         if_exists='append',
                                         index=False,
                                         dtype={'geom': Geometry('POINT', srid='4326')})

        return table_name_looping

    def join_rest_gee(self, country):

        #qry_string_delete = "SELECT __famews_remove_tables('{}');".format(country.lower())
        qry_string_create = "SELECT __famews_join_tables('{}');".format(country.lower())

        # print(qry_string_delete,qry_string_create)

        connection = self.engine.connect()
        try:
            trans = connection.begin()
            # connection.execute(qry_string_delete)
            connection.execute(qry_string_create)
            trans.commit()
        except exc.SQLAlchemyError as esql:
            trans.rollback()
            return esql

        connection.close()

    def join_rest_gee_temp(self, country):

        # qry_string_delete = "SELECT __famews_remove_tables('{}');".format(country.lower())
        qry_string_create = "SELECT __famews_join_tables('{}');".format(country.lower())

        # print(qry_string_delete,qry_string_create)

        connection = self.engine.connect()
        try:
            trans = connection.begin()
            # connection.execute(qry_string_delete)
            connection.execute(qry_string_create)
            trans.commit()
        except exc.SQLAlchemyError as esql:
            trans.rollback()
            return esql

        connection.close()


    def data_export_GDrive(self, feature_collection_with_precipitation):
        # Export
        export_task = Export.table.toDrive(
                    collection = feature_collection_with_precipitation,
                    folder = "testExtract",
                    fileFormat = 'csv',
                    description = "testExtract")

        export_task.start()
        state=export_task.status()['state']

        while state in ['READY', 'RUNNING']:
            print(state + '...')
            state = export_task.status()['state']

        print('Done.', export_task.status())


    def plotting_scoutings_single_by_day(self, df_cio_gee_noDuplicates, list_of_dates):

        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        ax = world[world.continent == 'Africa'].plot(color='grey', edgecolor='white')
        cycle_colors = cycle('bgrcmk')

        for unique_date in list_of_dates:

            mask = (df_cio_gee_noDuplicates['date'] == unique_date)
            df_oneDay = df_cio_gee_noDuplicates.loc[mask]

            gdf_oneDay = gpd.GeoDataFrame(df_oneDay,
                                          geometry=gpd.points_from_xy(df_oneDay.longitude, df_oneDay.latitude))
            gdf_oneDay.drop([u'latitude', u'longitude'], axis=1, inplace=True)

            gdf_oneDay.plot(ax=ax, color='red', marker='*', markersize=3)
            gdf_oneDay.plot(ax=ax, color=cycle_colors.next(), marker='*', markersize=3)

        plt.show()


