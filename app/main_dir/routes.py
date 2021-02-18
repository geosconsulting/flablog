from flask import render_template, send_file

import base64
from io import BytesIO, StringIO
from matplotlib.figure import Figure

from . import main_bp

@main_bp.route('/')
@main_bp.route('/index')
def index():
    return render_template('main/index.html')

@main_bp.route('/i1')
def i1():
    return render_template('main/about.html')

@main_bp.route('/mpl')
def mpl():

    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1 , 2, 1, 5, 2, 4, 5])

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf , format="png")

    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

@main_bp.route('/images/<cropzonekey>')
def images(cropzonekey):
    return render_template("images.html", title=cropzonekey)

@main_bp.route('/fig/<cropzonekey>')
def fig(cropzonekey):
    fig = draw_polygons(cropzonekey)
    img = StringIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@main_bp.route('/geospatial')
def geospatial():
    return render_template('main/geospatial.html')

@main_bp.route('/data-analysis')
def dataanalysis():
    return render_template('main/data-analysis.html')

@main_bp.route('/remote-sensing')
def remotesensing():
    return render_template('main/remote-sensing.html')

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

