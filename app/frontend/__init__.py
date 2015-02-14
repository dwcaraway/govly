import logging
import os
from flask import Flask
_log = logging.getLogger(__name__)

root_directory = os.path.dirname(os.path.abspath(__file__))
assets_directory = os.path.join(root_directory, '../../dist')

def create_app(settings_override=None):
    """Returns front end Flask application instance"""
    from . import assets
    from . import extensions

    app = Flask(__name__, static_folder=assets_directory, static_url_path='')

    # Initialize settings
    app.config.from_object(settings_override)

    @app.route('/')
    def root():
        return app.send_static_file('index.html')

    # Init assets
    assets.init_app(app)

    # Flask-DebugToolbar
    extensions.debug_toolbar.init_app(app)

    _log.info("Flask frontend app created")
    return app

