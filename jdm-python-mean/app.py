from utils.calculator import Calculator
from flask import Flask, request
import json
import sys

sys.path.append(".")

# Create the Flask app
app = Flask(__name__)

@app.route('/mean',methods = ['POST'])
def mean():
    values =  json.loads(request.form.getlist("metadata")[0])

    calculator = Calculator()
    result = calculator.mean(values); 

    return result