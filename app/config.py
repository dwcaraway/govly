import os

class Config(object):
    """
    Configuration base, for all environments.
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    BOOTSTRAP_FONTAWESOME = True
    SECRET_KEY = "secret"
    CSRF_ENABLED = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_SALT = 'lotsofsalt'
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "%s/vitals" % os.getenv('OPENSHIFT_POSTGRESQL_DB_URL')
    #TODO remove the DEBUG = True statement before customers are on this!
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True