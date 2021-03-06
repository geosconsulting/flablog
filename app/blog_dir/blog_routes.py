from flask import render_template, request
# from flask_login import login_required

from . import blog_bp


@blog_bp.route('/sparc')
def sparc():
    return render_template('blog/sparc.html',title='SPARC')


@blog_bp.route('/grrasp')
def grrasp():
    return render_template('blog/grrasp.html')


@blog_bp.route('/famews')
def famews():
    return render_template('blog/famews.html',title='FAMEWS')


@blog_bp.route('/idai')
def idai():
    coords = [-19.831594 , 34.837017]
    zoom = 8
    return render_template('blog/cyclone_idai.html',coords=coords,zoom=zoom)


@blog_bp.route('/castelfusano')
def castelfusano():
    coords = [41.731163 , 12.321748]
    zoom = 11
    return render_template('blog/wildfire_cfusano.html',coords=coords,zoom=zoom)


@blog_bp.route('/giovanni')
def giovanni():
    coords = [41.885921 , 12.561899]
    zoom = 7
    return render_template('blog/giovanni-precipitation.html',coords=coords,zoom=zoom)


@blog_bp.route('/edit-blog', methods=['GET','POST'])
# @login_required
def edit_blog():
    if request.method == 'POST':
        data = request.form.get('ckeditor')
        print(data)
    return render_template('blog/blog-editor.html')