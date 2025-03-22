from app import mongo
from datetime import datetime
from bson import ObjectId
from flask import current_app

class Subject:
    @staticmethod
    def get_all():
        return list(mongo.db.subjects.find().sort('name', 1))

    @staticmethod
    def get_by_id(subject_id):
        return mongo.db.subjects.find_one({'_id': ObjectId(subject_id)})

    @staticmethod
    def get_by_name(name):
        return mongo.db.subjects.find_one({'name': name})

    @staticmethod
    def create(name, description=None):
        subject_data = {
            'name': name,
            'description': description,
            'created_at': datetime.utcnow()
        }
        result = mongo.db.subjects.insert_one(subject_data)
        subject_data['_id'] = result.inserted_id
        return subject_data

class Resource:
    @staticmethod
    def get_all():
        return list(mongo.db.resources.find())

    @staticmethod
    def get_by_id(resource_id):
        return mongo.db.resources.find_one({'_id': ObjectId(resource_id)})

    @staticmethod
    def get_by_subject(subject_id):
        return list(mongo.db.resources.find({'subject_id': ObjectId(subject_id)}))

    @staticmethod
    def get_by_author(author_id):
        return list(mongo.db.resources.find({'author_id': ObjectId(author_id)}))

    @staticmethod
    def create(title, description, filename, file_type, author_id, subject_id):
        resource = {
            'title': title,
            'description': description,
            'filename': filename,
            'file_type': file_type,
            'author_id': author_id,
            'subject_id': subject_id,
            'created_at': datetime.utcnow(),
            'is_verified': False,
            'verified_by': None,
            'verified_at': None,
            'views': 0,
            'downloads': 0
        }
        result = mongo.db.resources.insert_one(resource)
        resource['_id'] = result.inserted_id
        return resource

    @staticmethod
    def get_all_verified(page=1, per_page=12, subject=None, search=None):
        query = {'is_verified': True}
        
        if subject:
            query['subject_id'] = ObjectId(subject)
            
        if search:
            query['$or'] = [
                {'title': {'$regex': search, '$options': 'i'}},
                {'description': {'$regex': search, '$options': 'i'}}
            ]
        
        total = mongo.db.resources.count_documents(query)
        resources = mongo.db.resources.find(query) \
            .sort('created_at', -1) \
            .skip((page - 1) * per_page) \
            .limit(per_page)
            
        return {
            'items': list(resources),
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'page': page
        }

    @staticmethod
    def verify(resource_id, mentor_id):
        return mongo.db.resources.update_one(
            {'_id': ObjectId(resource_id)},
            {
                '$set': {
                    'is_verified': True,
                    'verified_by': mentor_id,
                    'verified_at': datetime.utcnow()
                }
            }
        )

    @staticmethod
    def increment_views(resource_id):
        return mongo.db.resources.update_one(
            {'_id': ObjectId(resource_id)},
            {'$inc': {'views': 1}}
        )

    @staticmethod
    def increment_downloads(resource_id):
        return mongo.db.resources.update_one(
            {'_id': ObjectId(resource_id)},
            {'$inc': {'downloads': 1}}
        )

    @staticmethod
    def search(query):
        return list(mongo.db.resources.find({
            '$and': [
                {'is_verified': True},
                {
                    '$or': [
                        {'title': {'$regex': query, '$options': 'i'}},
                        {'description': {'$regex': query, '$options': 'i'}}
                    ]
                }
            ]
        })) 