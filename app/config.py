import os

class Config(object):
    """
    Configuration base, for all environments.
    """
    DEBUG = False
    TESTING = False

    SECRET_KEY = "supermegavitalssecret"
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'ubersaltstuff'
    SECURITY_CONFIRMABLE = True

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_SSL = True
    MAIL_SUPPRESS_SEND = True
    MAIL_USERNAME = 'testuser'
    MAIL_PASSWORD = 'testpassword'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://vitals:vitals@localhost:5432/vitals'
    MAIL_SUPPRESS_SEND = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://vitals:vitals@localhost:5432/vitalsdev'
    DEBUG = True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://vitals:vitals@localhost:5432/vitalstest'
    TESTING = True