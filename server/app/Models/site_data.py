from datetime import datetime
from bson import ObjectId
from app.extensions import mongo

class SiteData:
    @staticmethod
    def create(user_id, url, data):
        try:
            site_data_id = mongo.db.site_data.insert_one({
                'user_id': user_id,
                'url': url,
                'website_name': data.get('website_name'),
                'logo_url': data.get('logo_url'),
                'data': {
                    'fonts': data.get('fonts'),
                    'colors': data.get('colors'),
                    'technologies': data.get('technologies'),
                    'analysis': data.get('analysis')
                },
                'created_at': datetime.utcnow()
            }).inserted_id
            return site_data_id
        except Exception as e:
            print(f"Error creating site data: {e}")
        return None


    @staticmethod
    def get_by_user(user_id):
        try:
            sites = mongo.db.site_data.find({'user_id': user_id})
            site_list = []
            for site in sites:
                site['_id'] = str(site['_id'])  # Convert ObjectId to string
                site_list.append(site)
            return site_list
        except Exception as e:
            print(f"Error retrieving site data by user: {e}")
            return []

    @staticmethod
    def get_previews_by_user(user_id):
        try:
            sites = mongo.db.site_data.find({'user_id': user_id}, {'website_name': 1, 'logo_url': 1})
            site_list = []
            for site in sites:
                site['_id'] = str(site['_id'])  # Convert ObjectId to string
                site_list.append(site)
            return site_list
        except Exception as e:
            print(f"Error retrieving site previews by user: {e}")
            return []


    @staticmethod
    def get(site_data_id):
        try:
            site = mongo.db.site_data.find_one({'_id': ObjectId(site_data_id)})
            if site:
                site['_id'] = str(site['_id'])  # Convert ObjectId to string
            return site
        except Exception as e:
            print(f"Error retrieving site data: {e}")
            return None

    @staticmethod
    def delete(site_data_id):
        try:
            mongo.db.site_data.delete_one({'_id': ObjectId(site_data_id)})
        except Exception as e:
            print(f"Error deleting site data: {e}")
