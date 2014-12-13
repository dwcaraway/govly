# -*- coding: utf-8 -*-
"""
    vitals.api.v1.orgs
    ~~~~~~~~~~~~~~~~~~~

    :author: Dave Caraway
    :copyright: © 2014-2015, Fog Mine LLC
    :license: Proprietary, see LICENSE for more details.

    templated from https://github.com/ryanolson/cookiecutter-webapp
"""
from flask.ext.restful import abort, reqparse
from flask import url_for
from app.api.base import BaseView, secure_endpoint
from app.models.model import Organization
from dougrain import Builder

import json

org_parser = reqparse.RequestParser()
org_parser.add_argument('q', type=str, help='Free-text search string', default="")
org_parser.add_argument('page', type=int, help='Page number of results', default=1)
org_parser.add_argument('per_page', type=int, help='Max number of items (up to 200) per page',default=20)
org_parser.add_argument('order', type=str,
                                        help='Sort alphabetically by business name, ASC is ascending, DESC is descending',
                                        default='asc')

class OrganizationsView(BaseView):
    """A complete Flask-Classy-based Organizations API resource."""

    def index(self):
        """Returns a Collection of Organizations."""
        args = org_parser.parse_args()

        pagination = Organization.query.paginate(page=args.page, per_page=args.per_page)
        response = Builder(url_for("v1.OrganizationsView:index", page=pagination.page))\
            .add_curie('r', url_for('v1.LinkRelationsView:index')+"/{rel}")\
            .set_property('total', pagination.total)

        if pagination.has_prev:
            response = response.add_link('prev', url_for("v1.OrganizationsView:index", page=pagination.prev_num))

        if pagination.has_next:
            response = response.add_link('next', url_for("v1.OrganizationsView:index", page=pagination.next_num))

        if pagination.total > 1 and pagination.has_prev:
            response = response.add_link('first', url_for("v1.OrganizationsView:index", page=1))
        if pagination.total > 1 and pagination.has_next:
            response = response.add_link('last', url_for("v1.OrganizationsView:index", page=pagination.pages))

        for business in pagination.items:
            response = response.add_link('r:organization', url_for("v1.OrganizationsView:get", id=business.id))

        return response.as_object()

    @secure_endpoint()
    def post(self):
        """Creates a new Organization."""
        data = org_parser.parse_args()
        org = Organization.create(**data)
        return org.to_dict(), 201

    def get(self, id):
        """Returns a specific of Organization."""

        org = Organization.get_or_404(id)

        response = Builder(url_for("v1.OrganizationsView:get", id=id))\
            .add_curie('r', url_for('v1.LinkRelationsView:index')+"/{rel}")\
            .add_link('r:organizations', url_for("v1.OrganizationsView:index", page=1))

        for key, value in org.to_dict().iteritems():
            response.set_property(key, value)

        return response.as_object()

    @secure_endpoint()
    def put(self, id):
        """Updates an existing Organization."""
        data = org_parser.parse_args()
        org = Organization.get(id)
        org.patch(**data)
        return org.to_dict(), 200

    @secure_endpoint()
    def delete(self, id):
        """Deletes an existing Organization."""
        org = Organization.get(id)
        if org is None:
            return '', 204
        if org.delete():
            return '', 204
        abort(409)
