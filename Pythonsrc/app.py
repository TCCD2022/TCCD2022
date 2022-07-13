import json

from flask import *
from relationPlots import *


app = Flask(__name__)

@app.route('/rp',methods = ['POST'])

def appController():
    values = json.loads(request.form.getlist("metadata")[0])
    values1 = relationPlots(values)
    return values1


if __name__ == '__main__':
 	app.run(host="0.0.0.0",port=5001,debug=True)