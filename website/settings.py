import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv(override=True)

class Settings:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_PERMANENT = False
    SESSION_PERMANENT_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)