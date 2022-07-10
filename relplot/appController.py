
from flask import *
from app import *


app = Flask(__name__)

@app.route('/rp',methods = ['POST'])

def appController():


    print("----------------------------------llegue---------------------------------")
    print()

    values1 = relationPlots()

    return values1


if __name__ == '__main__':
 	app.run(host="0.0.0.0",port=4001,debug=True)