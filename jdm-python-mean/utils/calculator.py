# from csv import reader
from matplotlib import pyplot as plt
from datetime import datetime
from pathlib import Path

import numpy as np
import csv
import statistics
import os.path
import sys
sys.path.append(".")

class Calculator:
    def __init__(self):
        self._data_sets = None
        self._results_array = []
        self._column_names = []

    def basic_mean(self, data):
        # Calculate the mean of the data
        mean = statistics.mean(data)

        return mean

    def mean(self, data):
        # Open the file
        with open("/code/media/{}".format(data["filename"]), "r") as data_file:
            # Read the document rows
            csv_reader = csv.DictReader(data_file)

            # column_names = [col["colname"] for col in data["col_ids"]]
            column_names = [col["colname"] for col in data["col_ids"] if col["type"] != "String"]
            self._column_names = column_names
            
            self._data_sets = self.create_data_sets(column_names)
            
            # Add all elements to its dictionary key
            for row in csv_reader:
                for column_name in row:
                    if column_name in column_names:
                        self._data_sets[column_name].append(row[column_name])

            # Calculate the mean of each dictionary key
            for key in self._data_sets.keys():
                # Parse str to float
                self._data_sets[key] = list(map(float, self._data_sets[key]))
                
                # Calculate the mean
                mean = statistics.mean(self._data_sets[key])

                # Add the mean to the results array
                self._results_array.append(mean)

                # Format the result
                self._data_sets[key] = mean

            
            # Plot data
            x_pos = np.arange(len(self._column_names))

            fig, ax = plt.subplots()

            fig.set_size_inches(18.5, 15)

            rects = ax.bar(x_pos, self._results_array)
            ax.set_title(data["title"])
            ax.set_xlabel(data["caption"])
            ax.set_ylabel('Column mean')

            ax.set_xticks(x_pos, self._column_names, rotation=90)

            # Add the height to each bar
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width()/2., height,
                        '%d' % int(height),
                        ha='center', va='bottom')

            # Save plot
            current_path = "/".join(data["filename"].split('/')[:-1])
            current_name = data["filename"].split('/').pop()

            date = str(datetime.now())

            path_name = "/code/media/{}/dvg--results-/{}/".format(current_path, current_name)

            file_name = path_name + data["title"] + date + ".pdf"

            if not (os.path.exists(path_name)):
                print('doesnt exists')
                new_path = Path(path_name)
                new_path.mkdir(parents = True)

            plt.savefig(file_name)
            plt.clf()

            return {"pdffile":[file_name], "format":["pdf"]}

    def create_data_sets(self, column_names):
        data_set = dict()

        for name in column_names:
            data_set[name] = []

        return data_set
        

    def test(self):
        # Open the file
        with open("exergamingresults.csv") as data_file:
            # Read the document rows
            csv_reader = csv.DictReader(data_file)

            testData = {"fileid":"7e49e7e6-9e87-4880-adee-45bccedd6893",
            "filename":"documents/2022/07/10/exergamingresults.csv","col_ids":[{"colid":"1","colname":"iSubj","type":"Integer","scale":"Discrete"},{"colid":"2","colname":"trial","type":"Integer","scale":"Discrete"},{"colid":"3","colname":"Age","type":"Integer","scale":"Discrete"}],"methodid":"3"}

            column_names = [col["colname"] for col in testData["col_ids"]]
            self._column_names = column_names
            
            self._data_sets = self.create_data_sets(column_names)
            
            # Add all elements to its dictionary key
            for row in csv_reader:
                for column_name in row:
                    if column_name in column_names:
                        self._data_sets[column_name].append(row[column_name])


            # Calculate the mean of each dictionary key
            for key in self._data_sets.keys():
                # Parse str to float
                self._data_sets[key] = list(map(float, self._data_sets[key]))

                # Calculate the mean
                mean = statistics.mean(self._data_sets[key])

                # Add the mean to the results array
                self._results_array.append(mean)

                # Format the result
                # self._data_sets[key] = "The mean of the data from column '{}' is: {}".format(key, mean)
                self._data_sets[key] = mean

            
            # Plot data
            x_pos = np.arange(len(self._column_names))
            plt.bar(x_pos, self._results_array)
            plt.title('Mean - Juan David Murillo')
            plt.xlabel('Column names')
            plt.ylabel('Column mean')

            plt.xticks(x_pos, self._column_names)
            plt.show()

            # Save plot
            current_path = "/".join(testData["filename"].split('/')[:-1])
            file_name = testData["filename"].split('/').pop()

            target_path = "/code/media/{}/jdm-mean/{}/".format(current_path, file_name)

            if not (os.path.exists(target_path)):
                print('doesnt exists')
                new_path = Path(target_path)
                new_path.mkdir(parents = True)

            plt.savefig(file_name)
            print(self._data_sets)