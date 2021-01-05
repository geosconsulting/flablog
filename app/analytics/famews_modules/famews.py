class FAMEWSApi(object):

    """
    General settings for data management of old API
    """

    def __init__(self):
        self._working_dir = ''
        self.url = 'https://fao.cloud.tyk.io/famews/submission/'
        self.headers = {'x-token': 'c4quqFetMzwqv2DV0vdiuH3vs1i8O8'}

        self.url_psu_scoutings = 'https://plantvillage.psu.edu/api/v1/scout_surveys'
        self.url_psu_traps = 'https://plantvillage.psu.edu/api/v1/traps'

        self._shape_path_directory = "/data/"

        self._shp_admin_0 = None
        self._shp_admin_1 = None
        self._shp_admin_2 = None
        self.txt_world_all_codes_gaul = None
        self._shape_fawrisk_tce = None

        #r"C:\Users\Fabio\Documents\Programmazione\PowerBI\FAWRisk\geodata\africa_tce\SSA_Admin2.shp"

    @property
    def adm0(self):
        """
        Get the country selected for analysis
        :return: shapefile of countries
        """
        return self._shp_admin_0

    @adm0.setter
    def adm0(self, admin0_part):
        """
        Set shapefile of countries
        :param admin0_part:
        :return:
        """
        self._shp_admin_0 = self._working_dir + self._shape_path_directory + admin0_part

    @property
    def adm1(self):
        return self._shp_admin_1

    @adm1.setter
    def adm1(self, admin1_part):
        self._shp_admin_1 = self._working_dir + self._shape_path_directory + admin1_part

    @property
    def adm2(self):
        return self._shp_admin_2

    @adm2.setter
    def adm2(self, admin2_part):
        self._shp_admin_2 = self._working_dir + self._shape_path_directory + admin2_part

    @property
    def fawrisk(self):
        return self._shape_fawrisk_tce

    @fawrisk.setter
    def fawrisk(self, fawrisk_shp):
        self._shape_fawrisk_tce = self._working_dir + self._shape_path_directory + fawrisk_shp

    @property
    def world_gaul(self):
        return self.txt_world_all_codes_gaul

    @world_gaul.setter
    def world_gaul(self, gaul_shp):
        self.txt_world_all_codes_gaul = self._working_dir + self._shape_path_directory + gaul_shp

    @property
    def working_dir(self):
        """
        Working directory of analysis
        :return: directory
        """
        return self._working_dir

    @working_dir.setter
    def working_dir(self, working_dir):
        """
        set the working directory of the analysis
        :param working_dir:
        :return:
        """
        self._working_dir = working_dir
