import seaborn as sns
from matplotlib import pyplot as plt
from pandas import *
from csv import reader
import numpy as np
from pathlib import Path
import os
import json
from datetime import datetime
"""
 This method returns the plot corresponding to the linear
 regression of the first two columns indicated in the received parameter
 Parameters:
 --------------------------------------------
 data: Object with the necessary information to construct the plot: file name, 
       column names, plot title and color of the linear regression line.
"""
def linearRegressionMethod(data):
    #Columns:
    columns = data["col_ids"][:2];
    x = []
    y = []
    indexX = int(columns[0]["colid"])
    indexY = int(columns[1]["colid"])
    # open file
    with open("/code/media/"+data["filename"], "r") as my_file:
    # pass the file object to reader()
        file_reader = reader(my_file)
        next(file_reader,None)
        # do this for all the rows
        for i in file_reader:
            array =  i[0].split(",")
            x.append(float(array[indexX]))
            y.append(float(array[indexY]))
    colorPlot = data["colour"]
    titlePlot = data["title"]
    tmp =  data["filename"].split("/")[:-1]
    currentPath = "/".join(tmp)
    currentNameFile = data["filename"].split("/").pop()
    print("currentPath...", currentPath)
    print("currentName...", currentNameFile)
    date = str(datetime.now())
    pathName = '/code/media/'+ currentPath +'dvg--results-/'+ currentNameFile + "/"
    fileName = pathName + data["title"]+ date +".pdf" 
    if (os.path.exists(pathName) == False):
        path = Path(pathName)
        path.mkdir(parents=True)
    #Plot
    sns.regplot(x, y,color=colorPlot).set(title=titlePlot)
    plt.savefig(fileName)
    print("linearRegression....",fileName)
    return {"pdffile":[fileName], "format":["pdf"]}

