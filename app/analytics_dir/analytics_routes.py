from flask import render_template, Response, request
import requests
from flask_login import login_required

from . import analytics_bp
from . import famews_data
from .forms import FetchRecordsForm


@analytics_bp.route('/faw_situation')
def faw_situation():
    return render_template('analytics/global_faw.html')


@analytics_bp.route('/flood_chart')
def flood_chart():
    return render_template('analytics/sparc.html')


@analytics_bp.route('/write_famews_data', methods=['GET', 'POST'])
@login_required
def write_famews_data():
    form = FetchRecordsForm()

    country = form.country.data
    to_db = form.write2db.data

    if form.validate_on_submit():
        if country:
            df_records = famews_data.get_api_data(country)

        if to_db:
            famews_data.write_data(df_records)

    return render_template('analytics/get_api_records.html' , title='Get Data from API' , form=form)


@analytics_bp.route('/get_famews_data/<string:country>')
def get_famews_data(country):
    df_merged = famews_data.get_data(country)
    df_json = df_merged.to_json(orient='records')
    response = Response(response=df_json , status=200 , mimetype="application/json")
    return response


@analytics_bp.route('/famews_chart')
def famews_chart():
    cntry = request.args.get('country')
    r = requests.get('https://restcountries.eu/rest/v2/alpha/' + cntry)
    return render_template('analytics/famews.html', country = r.json()['name'])