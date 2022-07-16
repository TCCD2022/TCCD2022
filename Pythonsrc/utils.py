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

def bar_chart_plot_method(data):
    columns = [c['colname'] for c in data['col_ids']]
    readFile = pd.read_csv('/code/media/'+data["filename"], usecols=columns)
    print("readFile...", readFile.iloc[:, 0])
    x = readFile.iloc[:, 0]
    y = readFile.iloc[:, 1]
    print("x...", x)
    print("y...", y)
    #x = ['Python', 'R', 'Node.js', 'PHP']
    ## Declaramos valores para el eje y
    #y = [50,20,35,47]
    plt.bar(x, y, color = data["Color"])
    plt.xlabel(data["titlex"])
    plt.ylabel(data["titley"])
    plt.title(data["titleplot"])
    tmp =  data["filename"].split("/")[:-1]
    cpath = "/".join(tmp)
    nameFile = data["filename"].split("/").pop()
    path = '/code/media/'+ cpath +'/dvg--results-/'+ nameFile + "/"
    name = path + data["titleplot"]+".pdf"
    if (os.path.exists(path) == False):
    	pathDir = Path(path)
    	pathDir.mkdir(parents=True) 
    plt.savefig(name, format = "pdf")
    print("Bar Chart Plot....",name)
    return {"pdffile":[name], "format":["pdf"]}

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

def histogram_method(data):
    '''
    This method returns a histogram plot between the selected variables
    Parameters:
        data: Object with the necessary information to construct the plot: file name, 
        column names, plot title, bins, xLabel, YLabel. 
    '''
    plt.clf()
    fileName = data["filename"]
    columnsToFind = data["variablehistogram"]
    cols = [columnsToFind]
    df = pd.read_csv('/code/media/'+fileName, usecols=cols)
    # Path for savin the figure
    date = datetime.now()
    date = str(date.strftime("%Y%m%d_%H%M%S"))
    user_filename = "histogramPDF"+date
    filename = get_filename(data['filename'],user_filename)
    if 'binsvalue' in data.keys():
        binsTotal = data['binsvalue']
    else:
        binsTotal = 'auto'
    # Histogram Plot
    n, bins, patches=plt.hist(df, bins=binsTotal)
    plt.ylabel("Probability")
    if 'title' in data.keys():
        plt.title(data['title'])
    else:
        plt.title("Default title")

    plt.xlabel(columnsToFind)
    plt.ylabel("count")
    plt.savefig(filename,format='pdf',bbox_inches='tight')
    print("Histogram plot....",filename)
    return {"pdffile":[filename], "format":["pdf"]}


def kde_method(data):
    if data["filename"]:
        readFile = pd.read_csv('/code/media/'+data["filename"])
    else:
        print("Datos no ingresados")
    print(readFile)
    if(data["image_width"] and data["image_height"]):
        sns.set(rc={'figure.figsize':(data["image_width"],data["image_height"])})
    if(data["title"] and data["xaxislabel"]):
        plot=sns.kdeplot(data=readFile, shade=True).set( xlabel = data["xaxislabel"], ylabel = "Density", title=data["title"])
    else:
        plot=sns.kdeplot(data=readFile, shade=True)
    tmp =  data["filename"].split("/")[:-1]
    cpath = "/".join(tmp)
    nameFile = data["title"]
    path = '/code/media/'+ cpath +'/dvg--results-/'+ nameFile + "/"
    name = path + data["title"]+".pdf"
    if (os.path.exists(path) == False):
    	pathDir = Path(path)
    	pathDir.mkdir(parents=True) 
    plt.savefig(name, format = "pdf",dpi=300)
    return {"pdffile":[name], "format":["pdf"]}