from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime
from app import create_app, mongo

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['resource_platform']

# Create collections
collections = ['users', 'subjects', 'resources']
for collection in collections:
    if collection not in db.list_collection_names():
        db.create_collection(collection)

# Create indexes
db.users.create_index('email', unique=True)
db.resources.create_index('title')
db.resources.create_index('subject_id')

# Create initial admin user
admin_user = {
    'email': 'admin@example.com',
    'password': generate_password_hash('admin123'),
    'name': 'Admin User',
    'role': 'admin',
    'is_verified': True,
    'created_at': datetime.utcnow()
}

# Check if admin user exists
if not db.users.find_one({'email': admin_user['email']}):
    db.users.insert_one(admin_user)
    print("Admin user created successfully!")
    print("Email:", admin_user['email'])
    print("Password: admin123")

# Create initial subjects
subjects = [
    {'name': 'Mathematics', 'description': 'Mathematics and its applications'},
    {'name': 'Physics', 'description': 'Physics and its principles'},
    {'name': 'Chemistry', 'description': 'Chemistry and its applications'},
    {'name': 'Biology', 'description': 'Biology and life sciences'},
    {'name': 'Computer Science', 'description': 'Computer Science and programming'},
    {'name': 'English', 'description': 'English language and literature'},
    {'name': 'History', 'description': 'World history and civilizations'},
    {'name': 'Geography', 'description': 'Physical and human geography'},
    {'name': 'Economics', 'description': 'Micro and macro economics'},
    {'name': 'Political Science', 'description': 'Political systems and governance'}
]

# Insert subjects if they don't exist
for subject in subjects:
    if not db.subjects.find_one({'name': subject['name']}):
        db.subjects.insert_one(subject)

def init_db():
    app = create_app()
    with app.app_context():
        # Create subjects collection
        subjects = [
            {
                'name': 'AI & Robotics',
                'description': 'Artificial Intelligence, Machine Learning, and Robotics resources',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Quantum Computing',
                'description': 'Quantum computing and quantum information theory resources',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Neural Networks',
                'description': 'Deep learning and neural network resources',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Machine Learning',
                'description': 'Machine learning algorithms and applications',
                'created_at': datetime.utcnow()
            },
            {
                'name': 'Data Science',
                'description': 'Data analysis, visualization, and statistics resources',
                'created_at': datetime.utcnow()
            }
        ]
        
        # Insert subjects if they don't exist
        for subject in subjects:
            if not mongo.db.subjects.find_one({'name': subject['name']}):
                mongo.db.subjects.insert_one(subject)
                print(f"Added subject: {subject['name']}")
            else:
                print(f"Subject already exists: {subject['name']}")
        
        print("\nDatabase initialization completed!")

if __name__ == '__main__':
    init_db()

print("\nDatabase initialization completed successfully!")
print("Collections created:", collections)
print("Indexes created for users and resources")
print("Initial subjects added to the database") 