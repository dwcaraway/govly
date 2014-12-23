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
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super secret key - override with instance configuration')

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
    SECURITY_CONFIRMABLE = True
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
    SECURITY_FLASH_MESSAGES = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'another super secret key'
    WTF_CSRF_ENABLED = False

    # Flask-Security email options
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = True
    SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = True
    SECURITY_SEND_REGISTER_EMAIL = True

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

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

    # Flask-Mail
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

class DevelopmentConfig(Config):
    DEBUG = True
