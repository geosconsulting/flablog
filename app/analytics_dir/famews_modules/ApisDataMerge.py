import pandas as pd

from .CIOApiData import ApiCioDataCollection
from .PSUApiData import ApiPsuDataCollection


class ApiMergeDataCollection(ApiCioDataCollection, ApiPsuDataCollection):

    def __init__(self):

        super(ApiMergeDataCollection, self).__init__()
        self._combined_df = None

    def combined_df(self):
        combined_df = pd.concat([self.cio_df, self.psu_df], sort=True)
        # combined_df['totalPlantsChecked'] = combined_df.loc[:, super()._COL_PLANTS_CHECKED].sum(axis=1)
        # combined_df['totalPlantsInfested'] = combined_df.loc[:, super()._COL_PLANTS_INFESTED].sum(axis=1)
        self._combined_df = combined_df
        return combined_df

    def combined_df_geo(self):
        combined_df_geo = self._combined_df[super()._DF_COLUMNS_GEE]
        combined_df_geo.loc[~(combined_df_geo[['lat', 'lng']] == 0).all(axis=1)]
        return combined_df_geo

    def write_2_sqlite(self,df_merged):

        # table_name = super().country_name + "_" + super()._TIMESTAMP_SUFFIX
        table_name = super().country_iso
        print(table_name)
        sqlite_connection = super()._SQLITE_ENGINE.connect()
        print(sqlite_connection)

        df_merged.to_sql(table_name.lower(),sqlite_connection,if_exists='replace')

        sqlite_connection.close()

    def write_2_pg(self , df_merged):
        # table_name = super().country_name + "_" + super()._TIMESTAMP_SUFFIX
        table_name = super().country_iso
        print(table_name)
        pg_connection = super()._PG_ENGINE.connect()
        print(pg_connection)
        df_merged.to_sql(table_name.lower() , pg_connection , if_exists='replace', schema='famews')

        pg_connection.close()