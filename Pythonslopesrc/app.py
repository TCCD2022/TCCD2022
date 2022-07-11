from flask import Flask, jsonify
from flask import request
import json
from slopeService import slope_method


app = Flask(__name__)


@app.route('/',methods = ['GET'])
def helloslope():
    return "helloWorld"
@app.route('/slope',methods = ['GET'])
def slope():
    result = slope_method()
    return result

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True) 