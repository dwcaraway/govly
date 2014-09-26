# Import flask dependencies
from flask import Blueprint, render_template, jsonify
from app.model import Event, Source, db
from dougrain import Builder
from datetime import datetime
from flask.ext.restful import reqparse, abort, Api, Resource
import logging

logger = logging.getLogger(__name__)

mod_api = Blueprint('api', __name__, url_prefix='/api')
api = Api(mod_api)

class Endpoints(Resource):
	"""Index of all endpoints"""

	def get(self):
		return Builder('/').add_curie('r', '/api/rels/{rel}') \
		.add_link('r:events', '/api/events') \
		.add_link('r:sources', '/api/sources') \
		.as_object()

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

		self.post_req_parse = reqparse.RequestParser()

		super(EventsList, self).__init__()

	def get(self):
		""" Returns a collection of events matching specified criteria """
		
		args = self.get_req_parse.parse_args()

		logger.debug("event_count=%d " % len(Event.query.all()))

		pagination = Event.query.paginate(page=args.page, per_page=args.per_page)
		response = Builder("/api/events?page=%d" % pagination.page).add_curie('r', "/api/rels/{rel}").set_property('total', pagination.total)

		if pagination.has_prev:
			response = response.add_link('prev', '/api/events?page=%d' % pagination.prev_num)		 

		if pagination.has_next:
			response = response.add_link('next', '/api/events?page=%d' % pagination.next_num)

		if pagination.total > 0:
			response = response.add_link('first', '/api/events?page=1').add_link('last', '/api/events?page=%d' % pagination.pages)

		for event in pagination.items:
			response = response.embed('r:event', Builder('/api/rel'))

		return response.as_object()

	def post(self):
		""" Creates a new event """
		event = Event('http://www.foo.com', 'Test', 'Dayton, OH', datetime.now())	
		db.session.add(event)
		db.session.commit()

		return Builder('/events/%d' % event.id).set_property('id', event.id).as_object(), 201

class SourcesList(Resource):
	"""Sources of events"""

	def get(self):
		""" Returns a collection of sources matching specified criteria """
		response = Builder('/api/sources').add_curie('r', "/api/rels/{rel}")
		return response.as_object() 

RELS = {
	"event":
{
    "$schema": "http://json-schema.org/schema#",

    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"}
    },
    "required": ["email"]
},

"source":
{
    "$schema": "http://json-schema.org/schema#",

    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"}
    },
    "required": ["email"]
},
"events":
{
	"to":"do"
},
"sources":
{
	"to":"do"
}
}

class LinkRelationsList(Resource):
	"""Link relations for resources of the API"""

	def get(self):
		"""Gets all link relations"""
		return RELS

class LinkRelations(Resource):
	"""Individual link relations"""

	def get(self, rel_id):
		schema = RELS.get(rel_id)

		if schema is None:
			abort(404, message="Rel {} doesn't exist".format(rel_id))
		else:
			return RELS[rel_id]

api.add_resource(EventsList, '/events', endpoint = 'events')
api.add_resource(SourcesList, '/sources', endpoint = 'sources')
api.add_resource(Endpoints, '/', endpoint="endpoints")
api.add_resource(LinkRelationsList, '/rels/')
api.add_resource(LinkRelations, '/rels/<string:rel_id>')

