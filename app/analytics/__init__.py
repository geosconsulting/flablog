from flask import Blueprint

analytics = Blueprint('analytics', __name__, url_prefix='/analytics', template_folder='../../templates')