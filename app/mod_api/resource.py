# Import flask dependencies
from datetime import datetime
import logging

from flask import Blueprint, request
from dougrain import Builder
from flask.ext.restful import reqparse, Api, Resource, abort

from app.model import Event, db, Business


logger = logging.getLogger(__name__)

mod_api = Blueprint('api', __name__, url_prefix='/api')
api = Api(mod_api)


class Endpoints(Resource):
    """Index of all endpoints"""

    def get(self):
        """Starting endpoint for all available endpoints"""
        return Builder('/').add_curie('r', '/rels/{rel}') \
            .add_link('r:events', '/api/events') \
            .add_link('r:sources', '/api/sources') \
            .add_link('r:businesses', '/api/businesses')\
            .set_property('welcome', 'Welcome to the Vitals API!')\
            .as_object()


class EventsList(Resource):
    """Events that are happening"""

    def __init__(self):
        self.get_req_parse = reqparse.RequestParser()
        #TODO test for q parameter and then uncomment below
        #self.getparser.add_argument('q', type=str, help='Free-text search string', default="")
        self.get_req_parse.add_argument('page', type=int, help='Page number of results', default=1)
        self.get_req_parse.add_argument('per_page', type=int, help='Max number of items (up to 200) per page',
                                        default=20)
        #TODO test for complete parameter and then uncomment
        #self.getparser.add_argument('complete', type=bool, help='True if complete events should be included in results, false otherwise', default=False)
        self.get_req_parse.add_argument('order', type=str, help='Sort order of events response. Ascending sorts from \
			most distrant past event first to present/future event; descending does the opposite', default='asc')

        self.post_req_parse = reqparse.RequestParser()

        super(EventsList, self).__init__()

    def get(self):
        """ Returns a collection of events matching specified criteria """

        args = self.get_req_parse.parse_args()

        pagination = Event.query.paginate(page=args.page, per_page=args.per_page)
        response = Builder("/api/events?page=%d" % pagination.page).add_curie('r', "/api/rels/{rel}").set_property(
            'total', pagination.total)

        if pagination.has_prev:
            response = response.add_link('prev', '/api/events?page=%d' % pagination.prev_num)

        if pagination.has_next:
            response = response.add_link('next', '/api/events?page=%d' % pagination.next_num)

        if pagination.total > 0:
            response = response.add_link('first', '/api/events?page=1')\
                .add_link('last','/api/events?page=%d' % pagination.pages)
        for event in pagination.items:
            response = response.add_link('r:event', '/api/events/%d' % event.id)

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


class BusinessesList(Resource):
    """Businesses in the area"""

    def __init__(self):
        self.get_req_parse = reqparse.RequestParser()
        #TODO test for q parameter and then uncomment below
        #self.getparser.add_argument('q', type=str, help='Free-text search string', default="")
        self.get_req_parse.add_argument('page', type=int, help='Page number of results', default=1)
        self.get_req_parse.add_argument('per_page', type=int, help='Max number of items (up to 200) per page',
                                        default=20)
        #TODO test for complete parameter and then uncomment
        self.get_req_parse.add_argument('order', type=str,
                                        help='Sort alphabetically by business name, ASC is ascending, DESC is descending',
                                        default='asc')

        self.post_req_parse = reqparse.RequestParser()

        super(BusinessesList, self).__init__()

    def get(self):
        """ Returns a collection of businesses matching specified criteria """

        args = self.get_req_parse.parse_args()

        pagination = Business.query.paginate(page=args.page, per_page=args.per_page)
        response = Builder("/api/businesses?page=%d" % pagination.page).add_curie('r', "/api/rels/{rel}").set_property(
            'total', pagination.total)

        if pagination.has_prev:
            response = response.add_link('prev', '/api/businesses?page=%d' % pagination.prev_num)

        if pagination.has_next:
            response = response.add_link('next', '/api/businesses?page=%d' % pagination.next_num)

        if pagination.total > 0:
            response = response.add_link('first', '/api/businesses?page=1').add_link('last',
                                                                                     '/api/events?page=%d' % pagination.pages)
        for business in pagination.items:
            response = response.add_link('r:business', '/api/businesses/%d' % business)

        return response.as_object()

class Businesses(Resource):
    """Endpoint for individual businesses"""

    def __init__(self):
        self.get_req_parse = reqparse.RequestParser()
        self.get_req_parse.add_argument('id', type=int, help='unique id of the business')

    def get(self, id):
        """Get business by id"""
        args = self.get_req_parse.parse_args()

        biz = Business.query.get(id)

        if biz is None:
            abort(404, message="Business %d doesn't exist" % id)
        else:
            b = Builder(request.path).add_curie('r', '/rels/{rel}')\
            .add_link('r:events', '/api/businesses?page=1').set_property('id', biz.id)

            return b.as_object()



api.add_resource(EventsList, '/events', endpoint='events')
api.add_resource(SourcesList, '/sources', endpoint='sources')
api.add_resource(BusinessesList, '/businesses', endpoint='businesses')
api.add_resource(Businesses, '/businesses/<int:id>', endpoint='business')
api.add_resource(Endpoints, '/', endpoint="endpoints")


