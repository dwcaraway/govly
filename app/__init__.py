import os
from app.config import DevelopmentConfig
    
def create_application(config_object=DevelopmentConfig):
    from flask import Flask
    application = Flask(__name__)
    application.config.from_object(config_object)
    application.config.from_envvar('vitals_settings', True)

    from app.model import db
    db.init_app(application)

    from app.routes import index
    application.add_url_rule('/', 'index', index)

    from app.error import not_found, internal_error
    application.error_handler_spec[None][404] = not_found
    application.error_handler_spec[None][500] = internal_error

    # Import a module / component using its blueprint handler variable (mod_api)
    from app.mod_api.resources import mod_api as api_module
    from app.mod_api.rels import mod_rel as rel_module

    # Register blueprint(s)
    application.register_blueprint(api_module)
    application.register_blueprint(rel_module)

    # Create a user to test with
    @application.before_first_request
    def create_user():
        db.create_all()
        # user_datastore.create_user(name='Nick Gerakines', email='nick@gerakines.net', password='password')
        db.session.commit()

    return application