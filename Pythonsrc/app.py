

import json
from flask import Flask, jsonify
from utils import *
from flask import request
from flask import *
from relationPlots import *


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

@app.route('/corr',methods = ['POST'])
def correlation_plot():
    values =  json.loads(request.form.getlist("metadata")[0])
    result = correlation_plot_method(values)
    return result

@app.route('/bc',methods = ['POST'])
def bar_chart_plot():
    values =  json.loads(request.form.getlist("metadata")[0])
    result = bar_chart_plot_method(values)
    return result

@app.route('/rp',methods = ['POST'])

def appController():
    values = json.loads(request.form.getlist("metadata")[0])
    values1 = relationPlots(values)
    return values1


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001,debug=True)

