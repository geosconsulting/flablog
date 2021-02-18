import wbdata
import datetime

print(wbdata.get_source())

print(wbdata.get_indicator(source=1))

print(wbdata.search_countries('united'))

print(wbdata.get_data("IC.BUS.EASE.XQ", country="USA"))

data_date = datetime.datetime(2010, 1, 1), datetime.datetime(2011, 1, 1)

print(wbdata.get_data("IC.BUS.EASE.XQ", country=["USA", "GBR"], data_date=data_date))

print(wbdata.search_indicators("gdp per capita"))

print(wbdata.get_incomelevel())

countries = [i['id'] for i in wbdata.get_country(incomelevel='HIC')]

indicators = {"IC.BUS.EASE.XQ": "doing_business", "NY.GDP.PCAP.PP.KD": "gdppc"}

df = wbdata.get_dataframe(indicators, country=countries, convert_date=True)

print(df.describe())

df1 = wbdata.get_dataframe(indicators, country=countries, convert_date=True)

print(df1.sort_index().groupby('country').last().corr())

from hdx.utilities.easy_logging import setup_logging
from hdx.hdx_configuration import Configuration
from hdx.data.dataset import Dataset

setup_logging()
Configuration.create(hdx_site='prod', user_agent='A_Quick_Example', hdx_read_only=True)
dataset = Dataset.read_from_hdx('acled-conflict-data-for-africa-1997-lastyear')
print(dataset.get_date_of_dataset())

datasets = Dataset.search_in_hdx('Population', rows=10) #'ACLED'
print(datasets)
resources = Dataset.get_all_resources(datasets)
print(resources)