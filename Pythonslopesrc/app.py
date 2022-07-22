import json
from flask import Flask, jsonify
from flask import request
from matplotlib import pyplot as plt
from pathlib import Path
import os
import json
from datetime import datetime
import pandas as pd
#from Pythonslopesrc.slopeService import slope_method


app = Flask(__name__)


@app.route('/', methods=['GET'])
def helloslope():
    print("Test API OK")
    return "helloWorld"


"""
    post: /slope
    This method calculates the equation of a line given two points p1(x1, y1), p2(x2, y2),
    graphs it and generates a pdf file with the graph.
"""


@app.route('/slope', methods=['POST'])
def slope():
    values = json.loads(request.form.getlist("metadata")[0])
    file_name = values["filename"]
    cols = [col['colname'] for col in values['col_ids']]
    df = pd.read_csv('/code/media/'+file_name, usecols=cols)

    # x1 = df[cols[0]][0]
    # x2 = df[cols[0]][1]

    # y1 = df[cols[1]][0]
    # y2 = df[cols[1]][1]

    # m = (y2-y1)/(x2-x1)
    # b = y1 - m*x1

    # print(m)
    # print(b)

    x = df[cols[0]]  # Array with x values of csv
    y = df[cols[1]]  # Array with y values of csv

    plt.plot(x, y)

    tmp = file_name.split("/")[:-1]
    current_path = "/".join(tmp)
    current_name_file = file_name.split("/")[-1].split('.')[0]

    date = str(datetime.now())
    path_name = '/code/media/' + current_path + \
        'dvg--results-/' + current_name_file + "/"
    file_name = path_name + values["title"] + date + ".pdf"

    if (os.path.exists(path_name) == False):
        path = Path(path_name)
        path.mkdir(parents=True)

    plt.savefig(file_name)
    plt.clf()
    print("file_name...", file_name)

    # result = slope_method(values)
    # return result
    return {"pdffile": [file_name], "format": ["pdf"]}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
