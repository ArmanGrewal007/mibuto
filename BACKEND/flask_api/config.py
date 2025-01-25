import os
from datetime import datetime, timedelta

instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance')
os.makedirs(instance_path, exist_ok=True)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', "my_precious")
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', "my_precious") 
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', "my_precious")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1) # Default is 15 minutes
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(instance_path, "main.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authorization"
    SECURITY_TOKEN_AUTHENTICATION_BACKENDS = "jwt"
    SECURITY_TOKEN_MAX_AGE = 3600  # Token valid for 1 hour