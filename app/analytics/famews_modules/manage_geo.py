import geopandas as gpd
import fiona
from shapely.geometry import Point, Polygon, MultiPolygon, shape

from famews import FAMEWSApi

class ManageGeoData(FAMEWSApi):

    def __init__(self):

        super(ManageGeoData, self).__init__()

    @staticmethod
    def check_if_point_in(lats, longs, coordinates_poly, poly_type):

        misplaced = 0
        geom_base = shape(coordinates_poly)
        # print geom_base.wkt

        if poly_type == 'Polygon':
            poly = Polygon(geom_base)
        else:
            poly = MultiPolygon(geom_base)

        indexes_misplaced = []
        row_counter = 0
        for pnt_coord in zip(longs, lats):
            pnt = Point(pnt_coord)
            test = pnt.within(poly)
            row_counter += 1
            if test is False:
                print("{} out of the country".format(pnt))
                indexes_misplaced.append(row_counter - 1)
                misplaced += 1

        return misplaced, indexes_misplaced

    @staticmethod
    def get_admin_areas(txt_shp_admin, country_name):

        shape_admin = gpd.read_file(txt_shp_admin)

        # print shape_admin
        # shape_admin_cntry = shape_admin.loc[shape_admin['ADM0_NAME'] == country_name]
        shape_admin_cntry = shape_admin.loc[shape_admin['ADM0_NAME'] == country_name]

        return shape_admin_cntry

    def get_admin_poly(self, level_adm, iso2):
        """
        Get the coordinates of the polygon of the country
        :param level_adm: country,region or province (0,1,2)
        :param iso2: country code
        :return:
        """

        if level_adm == 0:
            shp_admin = self._shp_admin_0
        elif level_adm == 1:
            shp_admin = self._shp_admin_1
        elif level_adm == 2:
            shp_admin = self._shp_admin_2
        else:
            shp_admin = self.txt_world_all_codes_gaul

        with fiona.open(shp_admin) as src:
            filtered = filter(lambda f: f['properties']['int_code_4'] == iso2, src)

        return filtered

    @staticmethod
    def map_gpd(gdp_shapes):

        def add_basemap(ax, zoom, url='http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'):
            xmin, xmax, ymin, ymax = ax.axis()
            basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom, url=url)
            ax.imshow(basemap, extent=extent, interpolation='bilinear')
            # restore original x/y limits
            ax.axis((xmin, xmax, ymin, ymax))

        # df = gdp_shapes.to_crs(epsg=3857)

        ax = gdp_shapes.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
        add_basemap(ax, zoom=10)

    def spatial_intersects_points_poly(self, df, cntry_name):

        admin_shapes = gpd.read_file(self.txt_shp_admin_0)
        admin_cntry = admin_shapes[admin_shapes.ADM0_NAME == cntry_name].geometry

        scoutings_from_api = [Point(xy) for xy in zip(df.longitude, df.latitude)]
        crs = {'init': 'epsg:4326'}
        scoutings_shapes = gpd.GeoDataFrame(df, crs=crs, geometry=scoutings_from_api)

        gdf_scoutings_within_country = scoutings_shapes[scoutings_shapes.geometry.within(admin_cntry)]

        return gdf_scoutings_within_country

    def spatial_joins_scoutings_administrative_polygons(self, admin_type, df_points, df_admin, cntry, datepart):

        admin_shapes = gpd.read_file(df_admin)

        scoutings_from_api = [Point(xy) for xy in zip(df_points.longitude, df_points.latitude)]
        crs = {'init': 'epsg:4326'}

        scoutings_shapes_gdp = gpd.GeoDataFrame(df_points, crs=crs, geometry=scoutings_from_api)

        gdf_scoutings_with_country = gpd.sjoin(scoutings_shapes_gdp, admin_shapes, how="inner", op='intersects')

        list_point_attributes = ['_id', 'date', 'created', 'modified',
                                 'country', 'region', 'locationName',
                                 'latitude', 'longitude',
                                 # 'cropFertilizer', 'cropFieldSize', 'cropFieldSizeUnit',
                                 # 'cropHealth', 'cropIrrigation', 'cropMain',
                                 # 'cropStage', 'cropSystem', 'cropVariety', 'dataCollected',
                                 # 'fawControlBiopesticideLitres', #'fawControlBiopesticideName',
                                 # 'fawControlUndertaken', 'fawCurrentDamage', 'fawLarvaeKilledByNaturalEnemies',
                                 # 'fawNaturalEnemies', 'fawPreviousDamage',  # 'fawResourcesDamage', #'fawResourcesPest',
                                 # 'pestStageFAW', 'sample1FAW', 'sample1PlantsChecked', 'sample2FAW',
                                 # 'sample2PlantsChecked', 'sample3FAW', 'sample3PlantsChecked', 'sample4FAW',
                                 # 'sample4PlantsChecked', 'sample5FAW', 'sample5PlantsChecked', 'totalFAW',
                                 # 'totalPlantsChecked', 'fawControlChemicalPesticideLitres',  # 'fawColumns4Cobdamage',
                                 # 'fawControlLocalTypes'
                                ]

        if admin_type == 'iso':
            list_admin_attributes = ['area_sqkm', 'ADM0_CODE', 'ADM0_NAME',
                                     'ADM1_CODE', 'ADM1_NAME', 'ADM2_CODE', 'ADM2_NAME']
        else:
            list_admin_attributes = ['ID']

        gdf_scoutings_country_selected_attributes = gdf_scoutings_with_country[
            list_point_attributes + list_admin_attributes]

        try:
            geocoded_countries_filename = 'outputs/adm_' + cntry + "_" \
                                          + datepart + "_" + admin_type + '.csv'
            gdf_scoutings_country_selected_attributes.to_csv(geocoded_countries_filename, encoding='utf8')
            file_created = True
        except IOError as e:
            geocoded_countries_filename = e
            file_created = False

        return file_created, geocoded_countries_filename
