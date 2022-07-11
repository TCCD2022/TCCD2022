import json
from flask import Flask, jsonify
from linearRegression import *
from flask import request


app = Flask(__name__)


"""
    post: /lr
    Projection of the linear regression of two columns of numbers.
"""
@app.route('/lr',methods = ['POST'])
def linearRegression():
    values =  json.loads(request.form.getlist("metadata")[0])
    result = linearRegressionMethod(values)
    return result

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001,debug=True)
