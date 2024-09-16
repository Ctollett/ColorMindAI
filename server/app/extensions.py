from flask_login import LoginManager
from flask_pymongo import PyMongo
# app/extensions.py
from flask_mail import Mail

login_manager = LoginManager()
mongo = PyMongo()
mail = Mail()

def configure_extensions(app):
    login_manager.init_app(app)
    mongo.init_app(app)
    mail.init_app(app)
    # Setup other extensions

