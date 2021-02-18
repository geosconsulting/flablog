"""
Prepare the data collection from API and convert ISO2 code in a country name
"""
from datetime import datetime
import pycountry
from sqlalchemy import create_engine


class DataCollectionDefaults:

    """
    General settings for data management of API
    """

    _PSU_API_TRAPS = 'https://plantvillage.psu.edu/api/v1/traps'
    _PSU_SCOUT_SURVEY_JSON = 'https://plantvillage.psu.edu/json/scout_surveys/scout_survey.json'
    _CIO_FAMEWS_SUBMISSION = 'https://fao.cloud.tyk.io/famews/submission/'
    _COL_PLANTS_INFESTED = ['station1_faw', 'station2_faw', 'station3_faw', 'station4_faw', 'station5_faw']
    _COL_PLANTS_CHECKED = ['sample1PlantsChecked', 'sample2PlantsChecked', 'sample3PlantsChecked',
                           'sample4PlantsChecked', 'sample5PlantsChecked']
    _COLUMNS_COORDINATES = ['lattitude', 'longitude']
    _DF_COLUMNS_GEE = ['id', 'date_of_survey', 'lat', 'lng', 'origin']
    _TIMESTAMP_SUFFIX = datetime.now().strftime("%Y%m%d_%H%M%S")

    _SQLITE_ENGINE = create_engine('sqlite:///instance/flablog.sqlite')
    _PG_ENGINE = create_engine('postgresql://postgres:antarone@localhost/flablog')

    def __init__(self):
        """
        Set position of shapefiles in __shape_admin_0,__shape_admin_1,__shape_admin_2
        """
        self.__shape_admin_0 = None
        self.__shape_admin_1 = None
        self.__shape_admin_2 = None

    @property
    def working_dir(self):
        """
        Working directory of analysis
        :return: directory
        """
        return self.__working_dir

    @working_dir.setter
    def working_dir(self, working_dir):
        """
        set the working directory of the analysis
        :param working_dir:
        :return:
        """
        self.__working_dir = working_dir

    @property
    def country_name(self):
        """
        The country for which the data will be selected
        :return:
        """
        return self.__country_name

    @country_name.setter
    def country_name(self, country_iso):
        """
        Set the country for selecting the records for
        :param country_iso: ISO2 Code
        :return: Nothing
        """

        if country_iso == 'TL':
            self.__country_name = 'East Timor'
        else:
            for country in list(pycountry.countries):
                try:
                    if country_iso == country.alpha_2:
                        self.__country_name = country.name
                except NameError:
                    print(NameError)

    @property
    def country_iso(self):
        """
        The iso code of the country for which the data will be selected
        :return:
        """
        return self.__country_iso

    @country_iso.setter
    def country_iso(self, country_iso):
        """
        Set the country for selecting the records for
        :param country_iso: ISO2
        :return: Nothing
        """
        self.__country_iso = country_iso

    @property
    def adm0(self):
        """
        Get the country selected for analysis
        :return: shapefile of countries
        """
        return self.__shape_admin_0

    @adm0.setter
    def adm0(self , working_dir):
        """
        Set shapefile of countries
        :return: Path to Admin 0 shapefile
        """
        self.__shape_admin_0 = working_dir + '/geodata/GAUL/g2015_2014_0/g2015_2014_0.shp'

    @property
    def adm1(self):
        return self._shp_admin_1

    @adm1.setter
    def adm1(self , working_dir):
        """
        Set shapefile of regions
        :return: Path to Admin 1 shapefile
        """
        self.__shape_admin_1 = working_dir + '/geodata/GAUL/g2015_2014_1/g2015_2014_1.shp'

    @property
    def adm2(self):
        return self.__shape_admin_2

    @adm2.setter
    def adm2(self , working_dir):
        """
        Set shapefile of povinces
        :return: Path to Admin 2 shapefile
        """
        self.__shape_admin_2 = working_dir + '/geodata/GAUL/g2015_2014_2/g2015_2014_2.shp'
