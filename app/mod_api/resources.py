# Import flask dependencies
from flask import Blueprint, render_template, jsonify
from app import app, Event, Source
from dougrain import Builder
from flask.ext.restful import reqparse, abort, Api, Resource

mod_api = Blueprint('api', __name__, url_prefix='/api')
api = Api(mod_api)

class EndpointsList(Resource):
	"""Index of all endpoints"""

	def get(self):
		return {}

class EventsList(Resource):
	"""Events that are happening"""

	def get(self, complete=False, q='', start=1, limit=20, order='asc'):
		""" Returns a collection of events matching specified criteria """
		events = Event.query.all()
		response = Builder("/api/events?page=1").add_curie('r', "/api/rels/{rel}")

		for event in events:
			response = response.embed('r:event', Builder('/api/rel'))

		return response.as_object()

class SourcesList(Resource):
	"""Sources of events"""

	def get(self):
		""" Returns a collection of sources matching specified criteria """
		response = Builder('/api/sources').add_curie('r', "/api/rels/{rel}")
		return response.as_object() 

api.add_resource(EventsList, '/events')
api.add_resource(SourcesList, '/sources')
