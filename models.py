"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()
DEFAULT_IMAGE_URL = 'http://joelburton.com/joel-burton.jpg'


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    '''Individual User'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    img_url = db.Column(db.String, nullable=False)

    posts = db.relationship('Post', backref='user') # add comment to User
    # TODO: Add check for unique first_name / last_name

    @property
    def full_name(self):
        ''' return full name of self '''

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    '''Individual Post'''

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
