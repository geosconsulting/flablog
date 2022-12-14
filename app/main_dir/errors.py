from flask import render_template, request, jsonify
from app.main_dir import main_bp
from app.analytics_dir import analytics_bp


@analytics_bp.app_errorhandler(401)
@main_bp.app_errorhandler(401)
def forbidden(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'unauthorized'})
        response.status_code = 401
        return response
    return render_template('main/401.html'), 401


@analytics_bp.app_errorhandler(403)
@main_bp.app_errorhandler(403)
def forbidden(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden'})
        response.status_code = 403
        return response
    return render_template('main/403.html'), 403


@analytics_bp.app_errorhandler(404)
@main_bp.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('main/404.html'), 404

@analytics_bp.app_errorhandler(500)
@main_bp.app_errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return render_template('main/500.html'), 500