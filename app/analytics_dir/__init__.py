from flask import Blueprint

analytics_bp = Blueprint('analytics_dir', __name__, url_prefix='/analytics_dir', template_folder='../../templates')