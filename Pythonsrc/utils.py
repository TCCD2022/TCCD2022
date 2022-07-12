import seaborn as sns
from matplotlib import pyplot as plt
from pandas import *
import pandas as pd
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
    plt.xlabel(nameX)
    plt.ylabel(nameY)
    plt.savefig(fileName)
    plt.clf()
    print("linearRegression....",fileName)
    return {"pdffile":[fileName], "format":["pdf"]}

def correlation_plot_method(data):
    '''
    This method returns a correlation plot between the selected variables
    Parameters:
        data: Object with the necessary information to construct the plot: file name, 
        column names, plot title and dimensions. 
    '''
    fileName = data["filename"]
    cols = [col['colname'] for col in data['col_ids']]
    df = pd.read_csv('/code/media/'+fileName, usecols=cols)
    # Path for savin the figure
    if 'save' in data.keys():
       user_filename = data['save']
    else:
        user_filename=''
    filename = get_filename(data['filename'],user_filename)
    # Correlation Plot
    plt.style.use('seaborn')
    annot = True if data['annot']=='Yes' else False
    sns.heatmap(df.corr(), annot = annot,cmap='RdYlBu',vmin=-1.0,vmax=1.0)

    if 'title' in data.keys():
        plt.title(data['title'])   
    plt.savefig(filename,format='pdf',bbox_inches='tight')
    plt.clf()
    print("Correlation plot....",filename)
    return {"pdffile":[filename], "format":["pdf"]}
    # pass

def get_filename(data_filename,user_filename):
    tmp =  data_filename.split("/")[:-1]
    currentPath = "/".join(tmp)
    currentNameFile = data_filename.split("/")[-1].split('.')[0] #Take the file name without extension
    print("currentPath...", currentPath)
    print("currentName...", currentNameFile)
    date = str(datetime.now().strftime('_%m%d%Y_%H%M')) #add month,day,year,hour,minute
    pathName = '/code/media/'+ currentPath +'/dvg--results-/'+ currentNameFile + "/"
    # Use default filename or a name setn by user
    if user_filename != '':
        fileName = pathName + user_filename +".pdf" 
    else:
        fileName = pathName + currentNameFile + date +".pdf" 

    if (os.path.exists(pathName) == False):
        path = Path(pathName)
        path.mkdir(parents=True)
    return fileName