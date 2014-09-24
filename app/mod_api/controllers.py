# Import flask dependencies
from flask import Blueprint, render_template, jsonify
from app import app
from dougrain import Builder
from flask.ext import restful

# Define the blueprint: 'api', set its url prefix: app.url/api
mod_api = Blueprint('api', __name__, url_prefix='/api')
api = restful.Api(mod_api)

class LinkRelations(restful.Resource):
	"""Link relations for resources of the API"""

	def get(self):
		return {'hello':'world'}

class Events(restful.Resource):
	"""Events that are happening"""

	def get(self, complete=False, q='', start=1, limit=20, order='asc'):
		""" Returns a collection of events matching specified criteria """
		response = Builder("/api/events")
		response.add_curie('r', "/api/rels/{rel}")

		return response.as_object() 

class Sources(restful.Resource):
	"""Sources of events"""

	def get(self):
		""" Returns a collection of sources matching specified criteria """
		response = Builder('/api/sources')
		return response.as_object() 

api.add_resource(Events, '/events')
api.add_resource(Sources, '/sources')
api.add_resource(LinkRelations, '/rels')
