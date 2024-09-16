# app/__init__.py
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from app.extensions import configure_extensions
from app.settings import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load config from the config file

    # Enable CORS
    CORS(app, supports_credentials=True, resources={r"/api/*": {
        "origins": "http://localhost:3000",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]  # Explicitly allowing OPTIONS
    }})

    # Initialize Bcrypt for password hashing
    bcrypt = Bcrypt(app)

    # Setup MongoDB Connection
    client = MongoClient(app.config['MONGO_URI'])
    app.db = client.get_default_database()

    # Register blueprints for different parts of the app
    from app.Routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api')

    from app.Routes.data_routes import main_bp
    app.register_blueprint(main_bp, url_prefix='/api')

    configure_extensions(app)
    return app

