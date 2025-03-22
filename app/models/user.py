from app import mongo, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bson.objectid import ObjectId

@login_manager.user_loader
def load_user(id):
    user_data = mongo.db.users.find_one({'_id': ObjectId(id)})
    return User(user_data) if user_data else None

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data.get('_id', ''))
        self.username = user_data.get('username', '')
        self.email = user_data.get('email', '')
        self.password_hash = user_data.get('password_hash', '')
        self.is_mentor = user_data.get('is_mentor', False)
        self.created_at = user_data.get('created_at')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        if not self.id:
            # New user
            user_data = {
                'username': self.username,
                'email': self.email,
                'password_hash': self.password_hash,
                'is_mentor': self.is_mentor,
                'created_at': self.created_at
            }
            result = mongo.db.users.insert_one(user_data)
            self.id = str(result.inserted_id)
        else:
            # Update existing user
            mongo.db.users.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {
                    'username': self.username,
                    'email': self.email,
                    'password_hash': self.password_hash,
                    'is_mentor': self.is_mentor
                }}
            )
        return self

    @staticmethod
    def get_by_username(username):
        user_data = mongo.db.users.find_one({'username': username})
        return User(user_data) if user_data else None

    @staticmethod
    def get_by_email(email):
        user_data = mongo.db.users.find_one({'email': email})
        return User(user_data) if user_data else None

    def __repr__(self):
        return f'<User {self.username}>' 