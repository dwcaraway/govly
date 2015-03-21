# -*- coding: utf-8 -*-
"""
    vitals.settings
    ~~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.
"""
import os

class Config(object):
    """
    Configuration base, for all environments.
    """

    # Flask
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'superdupersecret')
    MAX_INVITES = os.environ.get('MAX_INVITES', 5)

    PASSWORD_RESET_SALT = os.environ.get('PASSWORD_RESET_SALT', 'suw1gHvoZdYeKhVK0so_izb6J+1Yt=|=TeY2CbMQ_gxcMo9tEQST2qqqdgO4')

    CLIENT_DOMAIN = 'http://localhost:9000'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://vitals:vitals@localhost:5432/vitalsdev')

    # Framework
    USE_CDN = False
    USE_PJAX = False

    # Flask-DebugToolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Flask-Mail
    MAIL_SERVER = 'mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '278853aff981f06a9') #Mailtrap.io Username
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'a0fc2ab5a08c7f') #Mailtrap Test SMTP Key

    # Flask-Security basics
    SECURITY_CHANGEABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_RECOVERABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_TRACKABLE = True

    # Flask-Security redirects
    SECURITY_POST_CHANGE_VIEW = None
    SECURITY_POST_CONFIRM_VIEW = '/'
    SECURITY_POST_LOGIN_VIEW = '/'
    SECURITY_POST_LOGOUT_VIEW = '/'
    SECURITY_POST_REGISTER_VIEW = '/'
    SECURITY_POST_RESET_VIEW = None

    # Flask-Security options
    SECURITY_FLASH_MESSAGES = False
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'another super secret key'
    WTF_CSRF_ENABLED = False

    # Flask-Security email options
    SECURITY_EMAIL_SENDER = 'support@fogmine.com'
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = True
    SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = True

    # Flask-Security salt options
    SECURITY_CONFIRM_SALT = os.environ.get('EMAIL_CONFIRM_SALT', 'hL^50_mTOUWL_kv^QAg1%LMHL62jGtxrj^vfJUrBAjV1*Hc3AVuxsiqlG=Hj')
    SECURITY_RESET_SALT = os.environ.get('PASSWORD_RESET_SALT', 'suw1gHvoZdYeKhVK0so_izb6J+1Yt=|=TeY2CbMQ_gxcMo9tEQST2qqqdgO4')
    SECURITY_INVITE_SALT = os.environ.get('SECURITY_INVITE_SALT', 'iL0_mTOUWL_kv^QAg1%23kdkjhs0@===xrj^vfJUrBAjV1*Hc3AVux^iql=Hj')

    # Flask-Security token expiration options
    SECURITY_USE_INVITE_WITHIN = "90 days"

    # Celery
    CELERY_BROKER_URL= os.environ.get('REDISTOGO_URL', 'redis://127.0.0.1:6379')
    CELERY_RESULT_BACKEND=os.environ.get('REDISTOGO_URL', 'redis://127.0.0.1:6379')
    CELERYD_PREFETCH_MULTIPLIER=0
    CELERY_IMPORT = [
        'vitals.tasks',
    ]
    CELERY_INCLUDE = [
        'vitals.tasks',
    ]
    CELERYBEAT_SCHEDULE = {
    #   example of a celery beat entry
    #   'database-maintenence': {
    #       'task': 'vitals.tasks.database.maintenence',
    #       'schedule': crontab(minute=0, hour=4, day_of_month='*/3')
    #   }
    }

    #Flask-CORS
    CORS_ALLOW_HEADERS = ['Authorization', 'Content-Type'] #allow browsers to cross origin PUT and POST JSON, which is an OPTIONS followed by POST
    CORS_ALLOW_ORIGINS = 'http://localhost:9000'

    #Flask-JWT
    JWT_AUTH_URL_RULE = '/auth/login'
    JWT_AUTH_HEADER_PREFIX = 'Bearer'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

    CLIENT_DOMAIN = os.environ.get('CLIENT_DOMAIN', 'https://dash.fogmine.com')

    # Flask-Mail
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    #Flask-CORS
    CORS_ALLOW_ORIGINS='https://dash.fogmine.com'

    SECURITY_CHANGEABLE = False
    SECURITY_CONFIRMABLE = False
    SECURITY_RECOVERABLE = False
    SECURITY_REGISTERABLE = False
    SECURITY_TRACKABLE = True
    SECURITY_PASSWORDLESS = False

class StagingConfig(ProductionConfig):
    CLIENT_DOMAIN = os.environ.get('CLIENT_DOMAIN', 'https://staging.dash.fogmine.com')
    MAIL_SERVER = 'mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '278853aff981f06a9') #Mailtrap.io Username
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'a0fc2ab5a08c7f') #Mailtrap Test SMTP Key

class DevelopmentConfig(Config):
    DEBUG = True
