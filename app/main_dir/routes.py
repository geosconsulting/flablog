from flask import render_template, send_file

import base64
from io import BytesIO, StringIO
from matplotlib.figure import Figure
from flask_mail import Message


from . import main_bp
from app import mail


@main_bp.route('/')
@main_bp.route('/index')
def index():
    return render_template('main/index.html')


@main_bp.route('/sendem')
def sendem():
    msg = Message("Hello" ,
                  sender="fabio_100264@yahoo.it" ,
                  recipients=["fabiolana.notizie@gmail.com"])
    mail.send(msg)
    return 'Mail Sent'


@main_bp.route('/geospatial')
def geospatial():
    return render_template('main/geospatial.html')


@main_bp.route('/data-analysis')
def data_analysis():
    return render_template('main/data-analysis.html')


@main_bp.route('/remote-sensing')
def remote_sensing():
    return render_template('main/remote-sensing.html')


@main_bp.route('/about')
def about():
    return render_template('main/about.html')