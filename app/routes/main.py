from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import mongo
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    featured_resources = list(mongo.db.resources.find().sort('created_at', -1).limit(6))
    subjects = list(mongo.db.subjects.find())
    return render_template('index.html', 
                         featured_resources=featured_resources,
                         subjects=subjects)

@bp.route('/explore')
def explore():
    subject = request.args.get('subject')
    query = {'subject': subject} if subject else {}
    resources = list(mongo.db.resources.find(query).sort('created_at', -1))
    subjects = list(mongo.db.subjects.find())
    return render_template('explore.html', 
                         resources=resources,
                         subjects=subjects,
                         current_subject=subject)

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        resources = list(mongo.db.resources.find({
            '$or': [
                {'title': {'$regex': query, '$options': 'i'}},
                {'description': {'$regex': query, '$options': 'i'}},
                {'tags': {'$regex': query, '$options': 'i'}}
            ]
        }))
    else:
        resources = []
    return render_template('search.html', 
                         resources=resources,
                         query=query)

@bp.route('/profile')
@login_required
def profile():
    user_resources = list(mongo.db.resources.find({'author_id': current_user.id}))
    return render_template('profile.html', resources=user_resources) 