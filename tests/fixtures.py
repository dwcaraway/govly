__author__ = 'dave'

#This is seed data for the database. Used during development, usually run using manage.py

from mixer.backend.flask import mixer
from flask.ext.security.utils import encrypt_password
from datetime import datetime
from app.models.users import Role

def setup():
    role = Role.first(name='user') #Get the 'user' role or create it
    if not role:
       role = Role.create(name='user', description='provides basic system access', bitmask=2)

    mixer.blend('app.models.users.User', email="john.dott@myemail.com", password=encrypt_password('hello'),
                confirmed_at=datetime.now(), roles=[role])
    mixer.blend('app.models.users.User', email="bitter.s@provider.com", password=encrypt_password('world'),
                roles=[role])

