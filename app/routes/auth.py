from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo, login_manager
from datetime import datetime
from bson.objectid import ObjectId

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = mongo.db.users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            login_user(user)
            return redirect(url_for('main.index'))
        
        flash('Invalid username or password', 'danger')
    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if mongo.db.users.find_one({'username': username}):
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))
        
        if mongo.db.users.find_one({'email': email}):
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.register'))
        
        user = {
            'username': username,
            'email': email,
            'password': generate_password_hash(password),
            'created_at': datetime.utcnow()
        }
        
        mongo.db.users.insert_one(user)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return None
    
    # Create user object for Flask-Login
    user_obj = type('User', (), {
        'id': str(user['_id']),
        'username': user['username'],
        'is_authenticated': True,
        'is_active': True,
        'is_anonymous': False,
        'get_id': lambda self: str(user['_id'])
    })()
    return user_obj 