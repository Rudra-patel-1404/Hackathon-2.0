import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, current_app, send_from_directory, abort
from flask_login import login_required, current_user
from app import mongo
from datetime import datetime
from werkzeug.utils import secure_filename
from app.models.resource import Resource, Subject
from bson import ObjectId

bp = Blueprint('resources', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        subject = request.form.get('subject')
        tags = request.form.get('tags').split(',')
        file = request.files.get('file')
        
        if not all([title, description, subject, file]):
            flash('All fields are required', 'danger')
            return redirect(url_for('resources.upload'))
        
        # Save file
        filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        
        # Create resource document
        resource = {
            'title': title,
            'description': description,
            'subject': subject,
            'tags': [tag.strip() for tag in tags],
            'filename': filename,
            'file_path': file_path,
            'author_id': current_user.id,
            'created_at': datetime.utcnow(),
            'downloads': 0
        }
        
        mongo.db.resources.insert_one(resource)
        flash('Resource uploaded successfully!', 'success')
        return redirect(url_for('main.explore'))
    
    subjects = list(mongo.db.subjects.find())
    return render_template('upload.html', subjects=subjects)

@bp.route('/verify/<resource_id>', methods=['POST'])
@login_required
def verify_resource(resource_id):
    if not current_user.is_mentor:
        flash('Only mentors can verify resources', 'danger')
        return redirect(url_for('main.index'))
    
    result = Resource.verify(resource_id, current_user.id)
    if result.modified_count:
        flash('Resource verified successfully!', 'success')
    else:
        flash('Resource not found or already verified', 'warning')
    return redirect(url_for('main.index'))

@bp.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(
            current_app.config['UPLOAD_FOLDER'],
            filename,
            as_attachment=True
        )
    except FileNotFoundError:
        abort(404)

@bp.route('/view/<filename>')
def view_file(filename):
    try:
        return send_from_directory(
            current_app.config['UPLOAD_FOLDER'],
            filename
        )
    except FileNotFoundError:
        abort(404)

@bp.route('/resource/<resource_id>')
def view_resource(resource_id):
    resource = mongo.db.resources.find_one({'_id': resource_id})
    if not resource:
        flash('Resource not found', 'danger')
        return redirect(url_for('main.explore'))
    
    return render_template('resource.html', resource=resource)

@bp.route('/browse')
def browse():
    page = request.args.get('page', 1, type=int)
    per_page = 12
    resources = Resource.get_all_verified(page=page, per_page=per_page)
    subjects = Subject.get_all()
    return render_template('resources/browse.html', resources=resources, subjects=subjects) 