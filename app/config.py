class Config(object):
    """
    Configuration base, for all environments.
    """
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:////tmp/test.db'
    BOOTSTRAP_FONTAWESOME = True
    SECRET_KEY = "secret"
    CSRF_ENABLED = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_SALT = 'lotsofsalt'
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True