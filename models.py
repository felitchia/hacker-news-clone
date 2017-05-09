from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey


class Article(db.Model):

    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True)
    #user = ... will be a foreign key
    title = db.Column(db.String(60), nullable=False)
    text = db.Column(db.String, default = None)
    link = db.Column(db.String(100), default=None)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    votes = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime)

    def __init__(self, title, text, link, upvotes, downvotes, date):
        #self.user = user
        self.title = title
        if text is not None:
            self.text = text
            self.link = None
        elif link is not None:
            self.text = None
            self.link = link
        else:
            print('You must provide a link or text for the article')
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.votes = self.upvotes + self.downvotes
        self.date = date

    def __repr__(self):
        if self.text is not None:
            return "'%s'\n '%s')>" % (self.title, self.text)
        elif self.link is not None:
            return "'%s'\n '%s')>" % (self.title, self.link)

class User(db.Model):

    __tablename__ = "users"
    username = db.Column('username', db.String, primary_key=True, nullable=False, index=True)
    email = db.Column('email', db.String, nullable=False, unique=True, index=True)
    password = db.Column('pwhash', db.String, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    #Flask-login methods
    def is_authenticated(self):
        return True

    #Flask-login methods
    def is_active(self):
        return True

    #Flask-login methods
    def is_anonymous(self):
        return False

    #Flask-login methods - must return a unicode that uniquely identifies the user
    def get_id(self):
        return self.username

    def __repr__(self):
        return "<User(name='%s')>" % self.username
