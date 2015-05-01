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
                             "minLength":6,
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
                },
                    "token": {"type": ["string", "null"],
                      "minLength": 8,
                      "maxLength": 120
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
    },
    "v1.UserView.InvitationsView": {
        "POST": {
            "properties": {
                "email": {"type": "string", "format":"email"}
            },
            "required": ["email"],
            "additionalProperties": False
        }
    },
    "v1.AuthView:change": {
        "POST": {
        "properties": {
                "old": {
                    "type":"string",
                    "maxLength":32
                },
                "new": {
                    "type":"string",
                    "mimLength": 6,
                    "maxLength": 32
                }
           },
            "required": ["new", "old"],
            "additionalProperties": False
        }
    },
    "v1.AuthView:update": {
        "POST": {
            "properties": {
                "password": {"type": "string",
                             "minLength": 6,
                             "maxLength": 120
                },
                "token": {"type": "string",
                          "minLength": 8,
                          "maxLength": 120
                }
            },
            "required": ["token"],
            "additionalProperties": False
        }
    },
    "v1.AuthView:reset": {
        "POST": {
                        "properties": {
                    "token": {"type": "string",
                              "minLength": 8,
                              "maxLength": 120
                    },
                "password": {
                    "type":"string",
                    "minLength": 6,
                    "maxLength":32
                }
           },
            "required": ["password", "token"],
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

