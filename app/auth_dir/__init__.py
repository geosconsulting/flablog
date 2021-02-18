from flask import Blueprint

auth_bp = Blueprint('auth_dir', __name__, url_prefix='/auth_dir', template_folder='../../templates')

