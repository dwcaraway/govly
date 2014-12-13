from flask.ext.restful import Api, Resource, abort
from flask import Blueprint

from app.api.base import BaseView
from dougrain import Builder

__author__ = 'DavidWCaraway'

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
            "to": "do"
        },
    "sources":
        {
            "to": "do"
        },
    "organizations":
        {
            "to": "do"
        },
    "organization":
        {
            "to": "do"
        },
    "signup": {
        "post": {
            "$schema": "http://json-schema.org/schema#",

            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "password": {"type": "string"},
                "real_name": {"type": "string"}
            },
            "required": ["email", "password"]
        },
    }
}

class LinkRelationsView(BaseView):
    """Link relations for resources of the API"""

    route_base = '/rels/'

    def index(self):
        """Gets all link relations"""
        return RELS

    def get(self, id):
        """Gets individual link relation."""
        try:
            return RELS[id]
        except KeyError:
            abort(404)
