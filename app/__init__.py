from werkzeug.wsgi import DispatcherMiddleware
from . import api
from . import frontend


def create_app(override_settings=None):
    return DispatcherMiddleware(frontend.create_app(override_settings), {
        '/api': api.create_app(override_settings),
    })