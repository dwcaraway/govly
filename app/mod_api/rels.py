# Import flask dependencies
from flask import Blueprint, render_template, jsonify
from app import app
from flask.ext.restful import Resource, Api, abort

mod_rel = Blueprint('rels', __name__, url_prefix='/rels')
api = Api(mod_rel)

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

api.add_resource(LinkRelationsList, '/')
api.add_resource(LinkRelations, '/<string:rel_id>')
