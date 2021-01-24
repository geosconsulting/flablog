from flask import render_template, Response, request, redirect, url_for, flash
from sqlalchemy import create_engine
import pandas as pd
import requests
import folium

import app
from . import analytics
from . import famews_data


@analytics.route('/faw_situation')
def faw_situation():
    return render_template('analytics/global_faw.html')


@analytics.route('/get_flood_data')
def get_flood_data():
    engine = create_engine(app.config.Config.SQLALCHEMY_DATABASE_URI)
    con = engine.connect()
    df_all = pd.read_sql_table(con=con , table_name="annual_pop_flood")
    df_all['iso3'] = df_all['iso3'].str.strip()
    df_all['adm0_name'] = df_all['adm0_name'].str.strip()
    df_all['adm1_name'] = df_all['adm1_name'].str.strip()
    df_all['adm2_name'] = df_all['adm2_name'].str.strip()
    df_all.drop(columns=['id','adm1_code','adm2_code'], inplace=True)
   # one_country = df_all['iso3'] == 'AFG'
   # df = df_all[one_country]

    df_json = df_all.to_json(orient='records')
    response = Response(response=df_json, status=200, mimetype="application/json")
    return(response)

@analytics.route('/flood_chart')
def flood_chart():
    return render_template('analytics/sparc.html')

@analytics.route('/global_famews')
def global_famews():
    return render_template('analytics/global_faw.html')

@analytics.route('/write_famews_data/<string:country>')
def write_famews_data(country):
    try:
        df_merged = famews_data.write_data(country)
        message = "OK"
    except IOError():
        message = "Error"
    return (message)

@analytics.route('/get_famews_data/<string:country>')
def get_famews_data(country):
    df_merged = famews_data.get_data(country)
    df_json = df_merged.to_json(orient='records')
    response = Response(response=df_json , status=200 , mimetype="application/json")
    return (response)

@analytics.route('/famews_chart')
def famews_chart():
    cntry = request.args.get('country')
    r = requests.get('https://restcountries.eu/rest/v2/alpha/' + cntry)
    return render_template('analytics/famews.html', country = r.json()['name'])