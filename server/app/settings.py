# settings.py

class Config:
    DEBUG = True  # Set to False in production
    SECRET_KEY = 'your_very_secret_key'  # Change this for production
    MONGO_URI = 'mongodb+srv://coltontollett96:ZHuQ8BSxhdZ0KK2O@cluster0.j6sm45w.mongodb.net/project0?retryWrites=true&w=majority&appName=Cluster0'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'coltontollett96@gmail.com'
    MAIL_PASSWORD = 'chki oyxa bgjc mrvy '
    MAIL_DEFAULT_SENDER = 'coltontollett96@gmail.com'
