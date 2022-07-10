import seaborn as sns
from matplotlib import pyplot as plt
from pandas import *
from csv import reader
import numpy as np
from pathlib import Path
import os
import json
from datetime import datetime

def relationPlots():
    print("dataaa58548")

    # selecting style
    sns.set(style="ticks")

    # reading the dataset
    tips = sns.load_dataset('tips')

    sns.relplot(x="total_bill",
                y="tip",
                hue="day",
                size="size",
                data=tips)

    plt.savefig("/code/media/documents/2022/07/10/nenita.pdf")
    return {"pdffile":["/code/media/documents/2022/07/10/nenita.pdf"], "format":["pdf"]}
