from flask import Blueprint

main_bp = Blueprint('main_dir', __name__, template_folder='../../templates')

from app.main_dir import routes, errors

