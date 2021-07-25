from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# The UserMixin class ensures that the minimun requirements for this model to work with
# Flask-Login are met.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # When setting the index and unique parameters to True simultaneously, the columns will be
    # generated with index values, duplicate values are not allowed.
    # Generating indexes makes searches and queries quicker, but updating tables slower, this is
    # because the inexes must be updated too. For this, it is adviceable to only use indexes
    # in columns that will get queried a lot.
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # The relationship() function provides a relationship between two classes.
    # The first parameter is the class representing the target of the relationship.
    # The backref argument makes the relationship bilateral.
    # So, when quering User.posts, we'll get all the posts related to the user;
    # and when quering Post.author, we'll get the User object parent of the Post object ;)
    # The lazy parameter relates to the way the ralationship will be loaded.
    # Something I should read futher into, but won't right now.
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<user> {self.username}'
    
    # This method generates sets the password hash for storing it in its column.
    def set_password(self, password):
        # The generate_password_hash() function takes a string as a parameter and return another
        # string, which is a hash of the given string.
        self.password_hash = generate_password_hash(password)
    
    # This method corroborates that a given password matches the hash stored in the database.
    def check_password(self, password):
        # The check_password_hash() function takes as parameter, a hash (string) and a password (string)
        # and returns True if they match, and False otherwise.
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime(), default=datetime.now)
    # The following column will store the value of the id column of the parent User object.
    # Because it's not refering to the User model class, but the user talbe, it's in lowercase.
    user_id = db.Column(db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'<post> {self.title}'


# In order to keep track of logged in users, Flask-Login stores the users id
# in the browsers session (I think). For that reason we need to hand over the user's
# id to Flask-Login through the following function.
# Flask-Login will recognize the function by this decorator.
@login.user_loader
def load_user(id):
    # Because Flask-Login will enter a string as id, we need to convert it to an integer for the query.
    return User.query.get(int(id))
