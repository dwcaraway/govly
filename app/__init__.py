# Import flask and template operators
from flask import Flask, render_template, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
import logging

# Define the WSGI application object
app = Flask(__name__)

# Define the database functions
db = SQLAlchemy(app)
#TODO move these database models elsewhere
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

# Configurations
app.config.from_object('app.config')

@app.route('/')
def index():
	return render_template('index.html')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_api)
from app.mod_api.resources import mod_api as api_module
from app.mod_api.rels import mod_rel as rel_module

# Register blueprint(s)
app.register_blueprint(api_module)
app.register_blueprint(rel_module)

