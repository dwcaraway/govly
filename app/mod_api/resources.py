# Import flask dependencies
from flask import Blueprint, render_template, jsonify
from app import app, Event, Source
from dougrain import Builder
from flask.ext import restful

# Define the blueprint: 'api', set its url prefix: app.url/api
mod_api = Blueprint('api', __name__, url_prefix='/api')
api = restful.Api(mod_api)

class EventsList(restful.Resource):
	"""Events that are happening"""

	def get(self, complete=False, q='', start=1, limit=20, order='asc'):
		""" Returns a collection of events matching specified criteria """
		events = Event.query.all()
		response = Builder("/api/events").add_curie('r', "/api/rels/{rel}")

		for event in events:
			response = response.embed('r:event', Builder('/foo'))

		return response.as_object() 

class Sources(restful.Resource):
	"""Sources of events"""

	def get(self):
		""" Returns a collection of sources matching specified criteria """
		response = Builder('/api/sources').add_curie('r', "/api/rels/{rel}")
		return response.as_object() 

api.add_resource(EventsList, '/events')
api.add_resource(Sources, '/sources')
