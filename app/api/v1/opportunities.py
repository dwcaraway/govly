# -*- coding: utf-8 -*-
"""
    vitals.api.v1.orgs
    ~~~~~~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
from app.api.base import BaseView, secure_endpoint
from urllib2 import urlopen
from flask_restful import reqparse
from urllib import urlencode
import json

index_reqparse = reqparse.RequestParser()
index_reqparse.add_argument('q', type=str, help='Free-text search string', default="")
index_reqparse.add_argument('start', type=int, help='get the next [limit] results starting with this number (zero-indexed)', default=0)
index_reqparse.add_argument('limit', type=int, help='number of results to return per request', default=20)
index_reqparse.add_argument('data_source', type=str, help="get results only from a particular data source. As of "
                                                          "2014-04-10, the available sources are ‘FBO’ and "
                                                          "‘grants.gov’. Case sensitive.", default="")
index_reqparse.add_argument('show_closed', type=bool, help="include opportunities with deadlines that have already passed in the results", default=False)
index_reqparse.add_argument('show_noncompeted', type=bool, help="include opportunities with deadlines that have already passed in the results", default=False)

class OpportunitiesView(BaseView):
    """A complete Flask-Classy-based Opportunities API resource."""
    route_base = '/opps/'

    @secure_endpoint()
    def index(self):
        """Returns a Collection of Opportunities."""
        args = index_reqparse.parse_args()
        args.api_key = "8l3xbEmsQMq7AG7mXoSy3IuJAqehmWGRC754Otx7"

        url = 'http://api.data.gov/gsa/fbopen/v0/opps?%s' % urlencode(query=args)

        return json.loads(urlopen(url=url).read())


