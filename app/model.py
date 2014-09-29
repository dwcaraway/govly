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

    address1 = db.Column(db.String(300))
    address2 = db.Column(db.String(300))
    city = db.Column(db.String(100))
    state = db.Column(db.String(70))
    zip = db.Column(db.String(15))
    latitude = db.Column(db.Float)
    longitude =db.Column(db.Float)
    projection = db.Column(db.String(15))

    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

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
    name = db.Column(db.String(100))
    events = db.relationship('Event', backref='source',
                                lazy='dynamic')
    businesses = db.relationship('Business', backref='source',
                                lazy='dynamic')

    def __repr__(self):
        return '<Source %r>' % self.id

class Business(db.Model):
    """A data model for a business"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    phone = db.Column(db.String(25))
    website = db.Column(db.String(400))
    facebook = db.Column(db.String(400))
    twitter = db.Column(db.String(400))
    logo = db.Column(db.String(400))
    category = db.Column(db.String(200))
    description = db.Column(db.String(1200))

    address1 = db.Column(db.String(300))
    address2 = db.Column(db.String(300))
    city = db.Column(db.String(100))
    state = db.Column(db.String(70))
    zip = db.Column(db.String(15))
    latitude = db.Column(db.Float)
    longitude =db.Column(db.Float)
    projection = db.Column(db.String(15))

    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    source_data_id = db.Column(db.String(15))
    source_data_url = db.Column(db.String(400))
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))

    def __repr__(self):
        return '<Business %r>' % self.name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
