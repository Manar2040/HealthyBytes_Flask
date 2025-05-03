import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '48458548u4#gfgflf#dgofojd'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///healthy_bytes.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False