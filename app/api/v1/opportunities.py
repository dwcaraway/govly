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
import json

class OpportunitiesView(BaseView):
    """A complete Flask-Classy-based Opportunities API resource."""
    route_base = '/opps/'

    @secure_endpoint()
    def index(self):
        """Returns a Collection of Opportunities."""
        #todo proxy call to api.data.gov
        resp = urlopen(url='http://api.data.gov/gsa/fbopen/v0/opps?api_key=8l3xbEmsQMq7AG7mXoSy3IuJAqehmWGRC754Otx7')

        return json.loads(resp.read())


