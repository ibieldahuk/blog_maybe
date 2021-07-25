from flask import Flask
from config import Config
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
# We relate the config from the Flask class with the class we created.
app.config.from_object(Config)
# The CSRFProtect class from the Flask-WTF library enables CSRF protection globally.
# This class need a secret key, that is why I'm intializing it after the config object.
# Note that each form requires aditional settings: Check the templates!
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# Setting the login_view property is necessary to make the @login_decorator work.
# See more in routes.py.
login.login_view = 'login'

from app import routes, models
