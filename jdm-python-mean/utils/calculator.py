# from csv import reader
import csv
import statistics

import os
import sys
sys.path.append(".")

class Calculator:
    def __init__(self, data):
        self.data = data

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

    def test(self):
        print("hello")
        # Open the file
        with open("exergamingresults.csv") as data_file:
            # Read the document rows
            csv_reader = csv.DictReader(data_file)
            
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')



calculator = Calculator(23)
calculator.mean()