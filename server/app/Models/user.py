from flask_login import UserMixin
from bson import ObjectId
from app.extensions import mongo
from app.Models.site_data import SiteData

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
        self.password = user_data['password']
        self.is_verified = user_data.get('is_verified', False)

    @staticmethod
    def get(user_id):
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_data)
        return None

    @staticmethod
    def get_by_email(email):
        user_data = mongo.db.users.find_one({'email': email})
        if user_data:
            return User(user_data)
        return None

    @staticmethod
    def get_by_username(username):
        user_data = mongo.db.users.find_one({'username': username})
        if user_data:
            return User(user_data)
        return None

    @staticmethod
    def create(username, email, password):
        try:
            user_id = mongo.db.users.insert_one({
                'username': username,
                'email': email,
                'password': password,
                'is_verified': False
            }).inserted_id
            return User.get(user_id)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def add_site_data(self, url, data):
        try:
            site_data_id = SiteData.create(self.id, url, data)
            return site_data_id
        except Exception as e:
            print(f"Error adding site data: {e}")
            return None

    def get_all_site_data(self):
        try:
            return SiteData.get_by_user(self.id)
        except Exception as e:
            print(f"Error retrieving all site data: {e}")
            return []

    def delete_site_data(self, site_data_id):
        try:
            SiteData.delete(site_data_id)
        except Exception as e:
            print(f"Error deleting site data: {e}")

    def save(self):
        try:
            mongo.db.users.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {
                    'username': self.username,
                    'email': self.email,
                    'password': self.password,
                    'is_verified': self.is_verified
                }}
            )
            return True
        except Exception as e:
            print(f"Error saving user: {e}")
            return False
