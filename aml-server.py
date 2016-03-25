import os
import json
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

class AmlService(Resource):
    @payment.required(1000)
    def post(self):
        # Get parameters

        if not request.data:
        	return {"status": "error", "message": "please provide at least one filter"}

        filters = json.loads(request.data)
        _filter = {}
        data = []

        if "first_name" in request.data:
        	_filter["first_name"] = filters["first_name"]
        if "last_name" in request.data:
        	_filter["last_name"] = filters["last_name"]
        if "dob" in request.data:
        	_filter["dob"] = filters["dob"]
        if "nationality" in request.data:
        	_filter["nationality"] = filters["nationality"]
        if "group_type" in request.data:
        	_filter["group_type"] = filters["group_type"]

        if len(_filter) == 0:
        	return {"status": "error", "message": "please provide at least one valid filter"}

        client = MongoClient('mongodb://aml:aml@ds013559.mlab.com:13559/aml')
        db = client.aml
        cursor = db.targets.find(_filter)[0:10]

        if cursor:
        	for target in cursor:
        		del target["_id"]
        		data.append(target)
        		return {"status": "ok", "data": data}
        else:
        	return {"status": "error", "message": "error retrieving data"}

api.add_resource(AmlService, '/')

if __name__ == '__main__':
    app.run(debug=True)