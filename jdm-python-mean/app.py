from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

import json
from utils import *
import sys
sys.path.append(".")

# Import the functions or methods that we will use
# from mean.mean_api import MeanApi

# Create the Flask app
app = Flask(__name__)
# CORS(app)
# api = Api(app)

# Generate the endpoint routing
# api.add_resource(MeanApi, "/mean")

from utils.calculator import Calculator

# data = open("/utils/exergamingresults.csv")

# calculator = Calculator(data)
# # calculator.test()

@app.route('/mean',methods = ['POST'])
def mean():
    values =  json.loads(request.form.getlist("metadata")[0])

    calculator = Calculator()
    result = calculator.mean(values); 

    # result = linearRegressionMethod(values)
    return result