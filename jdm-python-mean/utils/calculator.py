# from csv import reader
from matplotlib import pyplot as plt
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

    def mean_put(self, data):
        # Calculate the mean of the data
        mean = statistics.mean(data)

        return mean

    def mean(self):
        print('   ')

        # # filename = data["filename"]
        # filename ='exergamingresults.csv'

        # # Open the file
        # with open("/code/media/{}".format(filename), "r") as data_file:
        #     # Read the document rows
        #     csv_reader = csv.DictReader(data_file)
            
        #     line_count = 0
        #     for row in csv_reader:
        #         if line_count == 0:
        #             print(f'Column names are {", ".join(row)}')
        

        # return mean

    def create_data_sets(self, column_names):
        data_set = dict()

        for name in column_names:
            data_set[name] = []

        return data_set
        

    def test(self):
        print("hello")
        # print(os.path.dirname())
        print(os.path.exists('exergamingresults.csv'))
        print("   ")

        # Open the file
        with open("exergamingresults.csv") as data_file:
            # Read the document rows
            csv_reader = csv.DictReader(data_file)

            testData = {"fileid":"7e49e7e6-9e87-4880-adee-45bccedd6893","filename":"documents/2022/07/10/exergamingresults.csv","col_ids":[{"colid":"1","colname":"iSubj","type":"Integer","scale":"Discrete"},{"colid":"2","colname":"trial","type":"Integer","scale":"Discrete"},{"colid":"3","colname":"Age","type":"Integer","scale":"Discrete"}],"methodid":"3"}

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




            print(self._data_sets)



calculator = Calculator()
calculator.test()