# Import flask dependencies
from flask import Blueprint, render_template, jsonify
from app import app, Event, Source
from dougrain import Builder
from flask.ext.restful import reqparse, abort, Api, Resource

mod_api = Blueprint('api', __name__, url_prefix='/api')
api = Api(mod_api)

class Endpoints(Resource):
	"""Index of all endpoints"""

	def get(self):
		return {}

class EventsList(Resource):
	"""Events that are happening"""

	def __init__(self):
		self.get_req_parse = reqparse.RequestParser()
		#TODO test for q parameter and then uncomment below
		#self.getparser.add_argument('q', type=str, help='Free-text search string', default="")
		self.get_req_parse.add_argument('page', type=int, help='Page number of results', default=1)
		self.get_req_parse.add_argument('per_page', type=int, help='Max number of items (up to 200) per page', default=20)
		#TODO test for complete parameter and then uncomment
		#self.getparser.add_argument('complete', type=bool, help='True if complete events should be included in results, false otherwise', default=False)
		self.get_req_parse.add_argument('order', type=str, help='Sort order of events response. Ascending sorts from \
			most distrant past event first to present/future event; descending does the opposite', default='asc')

		super(EventsList, self).__init__()

	def get(self):
		""" Returns a collection of events matching specified criteria """
		
		args = self.get_req_parse.parse_args()

		pagination = Event.query.paginate(page=args.page, per_page=args.per_page)
		response = Builder("/api/events?page=%d" % pagination.page).add_curie('r', "/api/rels/{rel}") \
		.add_link('next', '/api/events?page=%d' % pagination.next_num).add_link('prev', '/api/events?page=%d' \
		 % pagination.prev_num).add_link('first', '/api/events?page=1').add_link('last', '/api/events?page=%d' \
		  % pagination.pages)

		for event in pagination.items:
			response = response.embed('r:event', Builder('/api/rel'))

		return response.as_object()

class SourcesList(Resource):
	"""Sources of events"""

	def get(self):
		""" Returns a collection of sources matching specified criteria """
		response = Builder('/api/sources').add_curie('r', "/api/rels/{rel}")
		return response.as_object() 

api.add_resource(EventsList, '/events', endpoint = 'events')
api.add_resource(SourcesList, '/sources', endpoint = 'sources')
api.add_resource(Endpoints, '/')

