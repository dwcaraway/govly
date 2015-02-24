from flask.ext.restful import Api, Resource, abort
from flask import Blueprint

from app.api.base import BaseView
from dougrain import Builder

__author__ = 'DavidWCaraway'

RELS = {
    "event":
        {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"}
            },
            "required": ["email"]
        },

    "source":
        {
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
     "opps":
        {
            "to": "do"
        },
    "v1.AuthView:register": {
        "POST": {
            "properties": {
                "password": {"type": "string",
                             "minLength":8,
                             "maxLength":120
                             },
                "email": {"type": "string", "format":"email"},
                "firstName": {
                    "type":"string",
                    "maxLength":32
                },
                "lastName":{
                    "type":"string",
                    "maxLength":32
                }
            },
            "required": ["email", "password", "firstName", "lastName"],
            "additionalProperties": False
        },
    },
    "v1.AuthView:confirm": {
        "POST": {
            "properties": {
                "token": {"type": "string",
                          "minLength": 8,
                          "maxLength": 120
                        }
            },
            "required": ["token"],
            "additionalProperties": False
        }
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

