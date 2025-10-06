import os

class Config:
    SECRET_KEY = os.environ.get('SESSION_SECRET') or os.environ.get('SECRET_KEY', 'dev_secret_key_plancheck_2024')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
