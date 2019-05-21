from flask import Flask, request, Response
from flask_restful import Resource, Api
from flask_restful import reqparse
import SVN
import os
import json

app = Flask(__name__)
api = Api(app)


class DataStore(Resource):
	def get(self,collection,object_id):
		result={}
		result=backend.getFile(collection,object_id)
		return Response(result, mimetype='text/plain')
class Collections(Resource):
	def get(self):
		result={}
		result=backend.getCollections()
		return result

class Search(Resource):
	def get(self):
		result={}
		parser = reqparse.RequestParser()
		parser.add_argument('q')
		parser.add_argument('c')
		args = parser.parse_args()
		result=backend.search(args['q'],args["c"])
		return result

backend=SVN.SVNBackend("testdir/workdir","testdir/repo")

api.add_resource(Collections, '/store/')
api.add_resource(DataStore, '/store/<collection>/<object_id>')
api.add_resource(Search, '/search/')


if __name__ == '__main__':
     app.run(port='5002')