import csv

import pandas
import seaborn as sns
from matplotlib import pyplot as plt
from pandas import *
from csv import reader
import numpy as np
from pathlib import Path
import os
import json
from datetime import datetime

def relationPlots(data):
    excelPath = "/code/media/"+data["filename"]

    x = data["col_ids"][0]
    y = data["col_ids"][1]

    sns.set(style="ticks")
    cvs = pandas.read_csv(excelPath)
    try:
        sns.relplot(x=x["colname"],
        y=y["colname"],
        hue="old",
        data=cvs).set(title=data["title"])
    except:
        sns.relplot(x=x["colname"],
                    y=y["colname"],
                    #hue="old",
                    data=cvs).set(title=data["title"])

    path = data["filename"].split("/")
    pathFinal = ""
    for i in range (len(path)-1):
        pathFinal+=path[i];
        pathFinal+="/"


    inMomory = "/code/media/{}{}.pdf".format(pathFinal, data["title"])
    print(inMomory)

    plt.savefig(inMomory)
    return {"pdffile":[inMomory], "format":["pdf"]}
