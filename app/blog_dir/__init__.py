from flask import Blueprint

blog_bp = Blueprint('blog_dir', __name__, url_prefix='/blog_dir', template_folder='../../templates')