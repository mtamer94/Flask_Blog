from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # this will be our unique ID
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg') # image will be hashed into 20 characters
    password = db.Column(db.String(60), nullable=False) # password will be hashed into 60 characters
    posts = db.relationship('Post', backref='author', lazy=True)
# with posts, we are saying that our post attribute has a relationship to the post Model
# the backref is similar to adding another column to the post Model
# it allows us to go back and see the user who created the posts
# lazy true means that SQL alchemy will load the data as necessary in one go, it will allow us to grab all posts by an author
# posts is not a column, it is a relationship
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

# below we are creating what is called a dunder method (double underscore) or magic method
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) # this will be our unique ID
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
# You always want to use UTC when saving times to a DB because they are consistent
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # ID of user who authored post

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
