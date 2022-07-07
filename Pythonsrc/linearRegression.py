import seaborn as sns
from matplotlib import pyplot as plt
from pandas import *
from csv import reader
import numpy as np
from pathlib import Path
import os
import json
def linearRegressionMethod(data):
    #Columns:
    columns = data["col_ids"][:2];
    x = []
    y = []
    indexX = int(columns[0]["colid"])
    indexY = int(columns[1]["colid"])
    print("indexY....",indexY)
    # open file
    with open("/code/media/"+data["filename"], "r") as my_file:
    # pass the file object to reader()
        file_reader = reader(my_file)
        next(file_reader,None)
        # do this for all the rows
        for i in file_reader:
            array =  i[0].split(",")
            # print the rows
            x.append(float(array[indexX]))
            y.append(float(array[indexY]))
    colorPlot = data["colour"]
    titlePlot = data["title"]

    pathName = 'code/media/dvg--results-/'
    if (os.path.exists(pathName) == False):
    	path = Path(pathName)
    	path.mkdir(parents=True)
    fileName = pathName + data["title"]+".pdf"
    #Plot
    sns.regplot(x, y,color=colorPlot).set(title=titlePlot)
    plt.savefig(fileName)
    print("linearRegression....",fileName)
    return {fileName, "pdf"}
