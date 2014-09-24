# Import flask dependencies
from flask import Blueprint, render_template
from app import app
from flask.ext import restful

# Define the blueprint: 'api', set its url prefix: app.url/api
mod_api = Blueprint('api', __name__, url_prefix='/api')
api = restful.Api(mod_api)

class HelloWorld(restful.Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
