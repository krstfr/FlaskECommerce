import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Nice try. Go home'
    SQLALCHEMY_DATABASE_URI= os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS= os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    CLOUDINARY_URL=os.environ.get('CLOUDINARY_URL')
