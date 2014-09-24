# Import flask dependencies
from flask import Blueprint, render_template
from app import app
from flask.ext import restful

# Define the blueprint: 'api', set its url prefix: app.url/api
mod_api = Blueprint('api', __name__, url_prefix='/api')
api = restful.Api(mod_api)

class Events(restful.Resource):
	def get(self, complete=False, q='', start=1, limit=20, order='asc'):
		""" Returns a collection of events matching specified criteria """
		return {'hello': 'world'}

class Sources(restful.Resource):
	def get(self):
		return {'hey': 'test'}

api.add_resource(Events, '/events')
api.add_resource(Sources, '/sources')
