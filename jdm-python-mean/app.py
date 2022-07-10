from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

import sys
sys.path.append(".")

# Import the functions or methods that we will use
from mean.mean_api import MeanApi

# Create the Flask app
app = Flask(__name__)
CORS(app)
api = Api(app)

# Generate the endpoint routing
api.add_resource(MeanApi, "/mean")