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
 rregression of the first two columns indicated in the received parameter
 Paraameters:
 --------------------------------------------
 data: Object with the necessary information to construct the plot: file name, 
       column names, plot title and color of the linear regression line.
"""
def linearRegressionMethod(data):
    #Columns:
    columns = data["col_ids"][:2];
    x = []
    y = []
    indexX = ""
    indexY = ""
    nameX = columns[0]["colname"].replace('"','')
    nameY = columns[1]["colname"].replace('"','')
    #print("Name X ", nameX)
    #print("Name Y ", nameY)
    # open file
    with open("/code/media/"+data["filename"], "r") as my_file:
    # pass the file object to reader()
        file_reader = reader(my_file)
        head =  next(file_reader,None)
        #head =  head[0]
        print("HEAD ", head)
        for i in range(0,len(head)):
            print("HEAD i ", head[i])
            if (head[i].replace('"','') == nameX ):
                indexX= i
                #print("If x ..", str(indexX))
            if (head[i].replace('"','') == nameY):
                indexY = i
                #print("If y...", str(indexY))
        # do this for all the rows
        for i in file_reader:
            #print("i..."+ str(i))
            array =  i
            #print("Array..."+ str(array))
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
    plt.clf()
    print("linearRegression....",fileName)
    return {"pdffile":[fileName], "format":["pdf"]}

