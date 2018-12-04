# /granules_index
# collection_url=URL
# collection_name=NAME

import sys
assert sys.version_info >= (3,6)

import time

from flask import Flask, request
from flask_restful import Resource, Api

# from flask.ext.jsonpify import jsonify


from granules_index import GranulesIndex

class GranulesIndexResource(Resource):
    def post(self):
        # get params
        collection_name = request.form['collection_name']  
        collection_xml_url = request.form['collection_xml_url']

        result = collection_xml_url
        result = GranulesIndex.index(collection_name, collection_xml_url)

        print(result)
        return result

    def get(self):
        collection_xml_url = request.args['collection_xml_url']
        start_time = request.args['start_time']
        end_time = request.args['end_time']

        print(collection_xml_url)
        print(start_time)
        print(end_time)
        result = GranulesIndex.get(collection_xml_url, start_time, end_time)

        # result = ""
        return result



application = Flask(__name__)
api = Api(application)

api.add_resource(GranulesIndexResource, '/granules_index') # Route_1

if __name__ == '__main__':
     application.run(port='8000', debug=True)
     