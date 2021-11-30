import os
# The basedir variable stores the main directory of the application.
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # The SECRET_KEY setting is used for protection from weird form related attacks.
    # Some CSRF stuff. I don't know.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLAlchemy takes the location of the app's database from the SQLALCHEMY_DATABASE_URI
    # config. Here, we take the database URL from the DATABASE_URL environment variable.
    # In case the DATABASE_URL variable isn't defined, we configure a database called
    #'app.db' in the main directory of the application.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABSE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
