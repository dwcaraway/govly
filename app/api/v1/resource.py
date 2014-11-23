# Import flask dependencies
from datetime import datetime
from datetime import date
import logging

from flask import Blueprint, request
from dougrain import Builder
from flask.ext.restful import reqparse, Api, Resource, abort

from app.models.model import Event, db, Organization, OrganizationSource


logger = logging.getLogger(__name__)

mod_api = Blueprint('api', __name__, url_prefix='/api')
api = Api(mod_api)

def log_exception(sender, exception, **extra):
    """ Log an exception to our logging framework """
    sender.logger.debug('Got exception during processing: %s', exception)

from flask import got_request_exception
got_request_exception.connect(log_exception, mod_api)


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

        if pagination.total > 1 and pagination.has_prev:
            response = response.add_link('first', '/api/events?page=1')
        if pagination.total > 1 and pagination.has_next:
            response = response.add_link('last','/api/events?page=%d' % pagination.pages)
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
    """Sources of data"""

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

        super(SourcesList, self).__init__()

    def get(self):
        """ Returns a collection of sources matching specified criteria """
        args = self.get_req_parse.parse_args()

        pagination = OrganizationSource.query.paginate(page=args.page, per_page=args.per_page)

        response = Builder("/api/sources?page=%d" % pagination.page).add_curie('r', "/api/rels/{rel}").set_property(
            'total', pagination.total)

        if pagination.has_prev:
            response = response.add_link('prev', '/api/sources?page=%d' % pagination.prev_num)

        if pagination.has_next:
            response = response.add_link('next', '/api/sources?page=%d' % pagination.next_num)

        if pagination.total > 1 and pagination.has_prev:
            response = response.add_link('first', '/api/sources?page=1')

        if pagination.total > 1 and pagination.has_next:
            response = response.add_link('last','/api/sources?page=%d' % pagination.pages)
        for source in pagination.items:
            response = response.add_link('r:source', '/api/sources/%d' % source.id)

        return response.as_object()

class Sources(Resource):

    def __init__(self):
        self.get_req_parse = reqparse.RequestParser()
        self.get_req_parse.add_argument('id', type=int, help='unique id of the Source')

    def get(self, id):
        """Get sources by id"""
        src = OrganizationSource.query.get(id)

        if src is None:
            abort(404, message="Source %d doesn't exist" % id)
        else:
            b = Builder(request.path).add_curie('r', '/rels/{rel}')\
            .add_link('r:sources', '/api/sources')

            for key, value in src.__dict__.iteritems():

                if isinstance(value, date):   
                    b = b.set_property(key, value.isoformat())
                elif value and key != '_sa_instance_state':
                    b = b.set_property(key, value)

            return b.as_object() 

class BusinessesList(Resource):
    """Businesses in the area"""

    def __init__(self):
        self.get_req_parse = reqparse.RequestParser()
        #TODO test for q parameter and then uncomment below
        self.get_req_parse.add_argument('q', type=str, help='Free-text search string', default="")
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

        pagination = Organization.query.paginate(page=args.page, per_page=args.per_page)
        response = Builder("/api/businesses?page=%d" % pagination.page).add_curie('r', "/api/rels/{rel}").set_property(
            'total', pagination.total)

        if pagination.has_prev:
            response = response.add_link('prev', '/api/businesses?page=%d' % pagination.prev_num)

        if pagination.has_next:
            response = response.add_link('next', '/api/businesses?page=%d' % pagination.next_num)

        if pagination.total > 1 and pagination.has_prev:
            response = response.add_link('first', '/api/businesses?page=1')
        if pagination.total > 1 and pagination.has_next:
            response = response.add_link('last', '/api/businesses?page=%d' % pagination.pages)

        for business in pagination.items:
            response = response.add_link('r:business', '/api/businesses/%d' % business.id)

        return response.as_object()

class Businesses(Resource):
    """Endpoint for individual businesses"""

    def __init__(self):
        self.get_req_parse = reqparse.RequestParser()
        self.get_req_parse.add_argument('id', type=int, help='unique id of the business', required=True)

    def get(self, id):
        """Get business by id"""

        biz = Organization.query.get(id)

        if biz is None:
            abort(404, message="Business %d doesn't exist" % id)
        else:
            b = Builder(request.path).add_curie('r', '/rels/{rel}')\
            .add_link('r:businesses', '/api/businesses?page=1')

            for key, value in biz.__dict__.iteritems():

                if isinstance(value, date):   
                    b = b.set_property(key, value.isoformat())
                elif value and key != '_sa_instance_state':
                    b = b.set_property(key, value)

            return b.as_object()

class SignUp(Resource):
    """Endpoint for signing up for an account"""

    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.req_parse.add_argument('email', type=str, help="The primary account email", required=True)
        self.req_parse.add_argument('password', type=str, help="The account password", required=True)

    def post(self):
        """Create a new account"""
        args = self.req_parse.parse_args()

        db.user_datastore.create_user(email=args['email'], password=args['password'])
        db.session.commit()

        return "Account created. A confirmation email has been sent.", 201



api.add_resource(EventsList, '/events', endpoint='events')
api.add_resource(SourcesList, '/sources', endpoint='sources')
api.add_resource(Sources, '/sources/<int:id>', endpoint='source')
api.add_resource(BusinessesList, '/businesses', endpoint='businesses')
api.add_resource(Businesses, '/businesses/<int:id>', endpoint='business')
api.add_resource(SignUp, '/signup', endpoint='signup')
api.add_resource(Endpoints, '/', endpoint="endpoints")

