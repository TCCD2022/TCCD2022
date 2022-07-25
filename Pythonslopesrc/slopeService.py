from matplotlib import pyplot as plt
from pathlib import Path
import os
import json
from datetime import datetime
import pandas as pd


def slope_method(values):
    file_name = values["filename"]
    cols = [col['colname'] for col in values['col_ids']]
    df = pd.read_csv('/code/media/'+file_name, usecols=cols)

    x1 = df[cols[0]][0]
    x2 = df[cols[0]][1]

    y1 = df[cols[1]][0]
    y2 = df[cols[1]][1]

    m = (y2-y1)/(x2-x1)
    b = y1 - m*x1

    plt.plot(df[cols[0]], df[cols[1]])
    print(m)
    print(b)

    tmp = file_name.split("/")[:-1]
    current_path = "/".join(tmp)
    # Take the file name without extension
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

    return {"pdffile": [file_name], "format": ["pdf"]}
