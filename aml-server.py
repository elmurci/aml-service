#!/usr/bin/env python3

import os
import json
import yaml
import config
from flask import Flask, request, abort, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson.json_util import dumps
from bson import json_util
from bson import ObjectId


#import from the 21 Developer Library
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

# set up server side wallet
app = Flask(__name__)
api = Api(app)

wallet = Wallet()
payment = Payment(app, wallet)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class ManifestService(Resource):	
    def get(self):
	    # Serves the app manifest to the 21 crawler.
	    with open('manifest.yaml', 'r') as f:
	        manifest_yaml = yaml.load(f)
	    return json.dumps(manifest_yaml)

class DbService():	
    def mongodb_conn():
	    try:
	        conn = MongoClient(config.mongo['connection'])
	    except pymongo.errors.ConnectionFailure as e:
	        print ("Could not connect to server: %s" % e)
	    return conn  

class AmlClient(Resource):
    def get(self):
    	return send_from_directory('static', 'aml-client.py')
    
class AmlService(Resource):
    @payment.required(config.payment['fee'])
    def get(self):

        # Get parameters
        if not request.args:
        	return {"status": "error", "message": "please provide at least one filter"}

        _filter = {}
        data = []
        _first_name = request.args.get("first_name")
        _last_name = request.args.get("last_name")
        _dob = request.args.get("dob")
        _nationality = request.args.get("nationality")
        _group_type = request.args.get("group_type")

        if _first_name is not None and _first_name != "":
        	_filter["first_name"] = _first_name
        if _last_name is not None and _last_name != "":
        	_filter["last_name"] = _last_name
        if _dob is not None and _dob != "":
        	_filter["dob"] = _dob
        if _nationality is not None and _nationality != "":
        	_filter["nationality"] = _nationality
        if _group_type is not None and _group_type != "":
        	_filter["group_type"] = _group_type

        if len(_filter) == 0:
        	return {"status": "error", "message": "please provide at least one valid filter"}

        try:
        	client = DbService.mongodb_conn()
        except pymongo.errors.PyMongoError as msg:
        	return {"status": "error", "message": "could not connect to the aml database"}

        print(client)

        if client is None:
        	return {"status": "error", "message": "could not connect to the aml database"}
        	
        try:
        	db = client.aml
       		cursor = db.targets.find(_filter)[0:10]
       	except:
        	return {"status": "error", "message": "could not retrieve data"}

        if cursor:
        	for target in cursor:
        		del target["_id"]
        		data.append(target)
        	return {"status": "ok", "data": data}
        else:
        	return {"status": "error", "message": "error retrieving data"}

api.add_resource(AmlService, '/aml')
api.add_resource(AmlClient, '/client')
api.add_resource(ManifestService, '/manifest')

if __name__ == '__main__':
    app.run(debug=config.debug)