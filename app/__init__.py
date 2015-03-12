from werkzeug.wsgi import DispatcherMiddleware
from . import api
from . import frontend
from . import admin

def create_app(override_settings=None):
    return DispatcherMiddleware(frontend.create_app(override_settings), {
        '/api': api.create_app(override_settings),
        '/admin': admin.create_app(override_settings)
    })