__author__ = 'dave'

#This is seed data for the database. Used during development, usually run using manage.py

from mixer.backend.flask import mixer
from flask.ext.security.utils import encrypt_password
from datetime import datetime
from app.models.users import Role, User

def setup():
    userRole = Role.first(name='user') #Get the 'user' role or create it
    if not userRole:
       userRole = Role.create(name='user', description='provides basic system access', bitmask=2)

    adminRole = Role.first(name='admin') #Get the 'admin' role or create it
    if not adminRole:
       adminRole = Role.create(name='admin', description='provides admin level system access', bitmask=4)


    if not User.first(email="john.dott@myemail.com"):
        mixer.blend('app.models.users.User', email="john.dott@myemail.com", password=encrypt_password('hello'),
                confirmed_at=datetime.now(), roles=[userRole])

    if not User.first(email="bitter.s@provider.com"):
        mixer.blend('app.models.users.User', email="bitter.s@provider.com", password=encrypt_password('world'),
                roles=[userRole])

    if not User.first(email="admin@fogmine.com"):
        mixer.blend('app.models.users.User', email="admin@fogmine.com", password=encrypt_password('supersecret'),
                roles=[adminRole])