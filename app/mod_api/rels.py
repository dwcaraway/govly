# Import flask dependencies
from flask import Blueprint, render_template, jsonify
from app import app
from flask.ext import restful

mod_rel = Blueprint('rels', __name__, url_prefix='/rels')
api = restful.Api(mod_rel)

RELS = {
	"event":{"id":"a unique identifier"},
	"source":{"id":"a unique identifier"}
}

class LinkRelationsList(restful.Resource):
	"""Link relations for resources of the API"""

	def get(self):
		"""Gets all link relations"""
		return RELS

class LinkRelations(restful.Resource):
	"""Individual link relations"""

	def get(self, rel_name):
		return jsonify(RELS[rel_name])

api.add_resource(LinkRelationsList, '/')
api.add_resource(LinkRelations, '/<string:rel_name>')
