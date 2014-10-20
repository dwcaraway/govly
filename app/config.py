import os

class Config(object):
    """
    Configuration base, for all environments.
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = "secret"
    CSRF_ENABLED = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_SALT = 'lotsofsalt'
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://vitals:vitals@localhost:5432/vitals'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://vitals:vitals@localhost:5432/vitalsdev'
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://vitals:vitals@localhost:5432/vitalstest'
    TESTING = True