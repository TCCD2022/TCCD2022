from flask import Flask, jsonify
from flask import request
import json
from slopeService import slope_method


app = Flask(__name__)


@app.route('/',methods = ['GET'])
def helloslope():
    print("Holaaaaa///")
    return "helloWorld"
    
@app.route('/slope',methods = ['POST'])
def slope():
    # result = slope_method()
    return {"pdffile":["HolaMundo"], "format":["pdf"]}

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True) 