import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///temp.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY=os.environ.get('SECRET_KEY', 'very_secret_key')
    TIMEZONE='UTC'