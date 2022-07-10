# from csv import reader
import csv
import statistics

import os.path
import sys
sys.path.append(".")

class Calculator:
    def __init__(self, data):
        self.data = data

        self._data_sets = None

    def mean(self):
        # Calculate the mean of the data
        # mean = statistics.mean(self.data)

        print('   ')
        print('   ')
        print('   ')
        print(self.data)

        # filename = data["filename"]
        filename ='exergamingresults.csv'

        # Open the file
        with open("/code/media/{}".format(filename), "r") as data_file:
            # Read the document rows
            csv_reader = csv.DictReader(data_file)
            
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
        

        return mean

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
            self._data_sets = self.create_data_sets(column_names)
            
            # print(self._data_sets)

            line_count = 0
            for row in csv_reader:
                for column_name in row:
                    if column_name in column_names:
                        self._data_sets[column_name].append(row[column_name])
                # print(row)
                # break

            print(self._data_sets)
                
                # if line_count == 0:
                #     print(f'Column names are {", ".join(row)}')
                #     line_count += 1
                # else:
                #     print(row)
                #     line_count += 1



calculator = Calculator(23)
calculator.test()