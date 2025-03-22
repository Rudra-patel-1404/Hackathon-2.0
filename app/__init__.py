from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from config import Config
import os

# Initialize extensions
mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configure upload folder
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

    # Initialize extensions
    mongo.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Create uploads directory if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Create indexes for MongoDB collections
    with app.app_context():
        # Create unique indexes
        mongo.db.users.create_index('username', unique=True)
        mongo.db.users.create_index('email', unique=True)
        
        # Create regular indexes for better query performance
        mongo.db.resources.create_index([('title', 'text'), ('description', 'text')])
        mongo.db.resources.create_index('author_id')
        mongo.db.resources.create_index('subject_id')
        mongo.db.resources.create_index('created_at')
    
    # Register blueprints
    from app.routes import main, auth, resources
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(resources.bp, url_prefix='/resources')
    
    return app 