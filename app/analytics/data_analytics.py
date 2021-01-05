from flask import render_template, Response
from sqlalchemy import create_engine
import pandas as pd

import app
from . import analytics

@analytics.route('/get_flood_data')
def get_flood_data():
    engine = create_engine(app.config.Config.SQLALCHEMY_DATABASE_URI)
    con = engine.connect()
    df_all = pd.read_sql_table(con=con , table_name="annual_pop_flood")
    df_all['adm0_name'] = df_all['adm0_name'].str.strip()
    df_all['adm1_name'] = df_all['adm1_name'].str.strip()
    df_all['adm2_name'] = df_all['adm2_name'].str.strip()
   # one_country = df_all['iso3'] == 'AFG'
   # df = df_all[one_country]

    df_json = df_all.to_json(orient='records')
    response = Response(response=df_json, status=200, mimetype="application/json")
    return(response)

@analytics.route('/flood_chart')
def flood_chart():
    return render_template('analytics/flood_chart.html')



@analytics.route('/faw')
def faw():
    pass
