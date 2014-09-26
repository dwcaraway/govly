from flask.ext.sqlalchemy import SQLAlchemy
# Define the database functions
db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(80))
    retrieved = db.Column(db.DateTime)
    title = db.Column(db.String(120))
    description = db.Column(db.String(800))
    location = db.Column(db.String(250))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))

    def __init__(self, url, title, location, start, description=None, end=None):
        self.url = url
        self.title = title
        self.description = description
        self.location = location
        self.start = start
        self.end = end

    def __repr__(self):
        return '<Event %r>' % self.title

class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    events = db.relationship('Event', backref='source',
                                lazy='dynamic')

    def __repr__(self):
        return '<Source %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
