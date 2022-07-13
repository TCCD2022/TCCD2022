import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask

app = Flask(__name__)

def buildGraph():
    data = pd.read_csv("test.csv", sep=",")

    df = data [["school_name", "killed", "injured"]]

    vv = df.groupby("school_name")["killed", "injured"].mean()
    vv.plot.barh()
    plt.title('Number of children affected by school shootings in US')
    plt.savefig("test", format = "pdf")

@app.route('/nncBarGraphic' , methods = ['POST'])
def nncBarGraphic():
    buildGraph()
    return 'Done!'

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8088,debug=True)

#Under Construction