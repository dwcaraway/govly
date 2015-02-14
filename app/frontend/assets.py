__author__ = 'dave'
import os
from flask.ext.assets import Environment

root_directory = os.path.dirname(os.path.abspath(__file__))
assets_directory = os.path.join(root_directory, '../../dist')

def init_app(app):
    assets = Environment(app)
    assets.debug = app.config.get('DEBUG', False)
    assets.directory = app.static_folder
    assets.url = app.static_url_path
    assets.directory = app.static_folder
    assets.append_path(assets_directory)
    assets.append_path(app.static_folder)
