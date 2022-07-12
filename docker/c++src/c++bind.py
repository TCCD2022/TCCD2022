import json
from flask import Flask, jsonify
from utils import *
from flask import request


app = Flask(__name__)


"""
    post: /lr
    Projection of the linear regression of two columns of numbers.
"""
@app.route('/kmeans',methods = ['POST'])
def kmeans():
    values =  json.loads(request.form.getlist("metadata")[0])
    result = KMeansMethod(values)
    return result

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4001,debug=True)
