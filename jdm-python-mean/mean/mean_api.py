from flask_restful import Resource, reqparse, abort
import sys
sys.path.append("..")
from utils.calculator import Calculator

# Config the required parameters for the api method
mean_post_args = reqparse.RequestParser()
mean_post_args.add_argument("data", type=str, help="Data array is required", required=True)

class MeanApi(Resource):
    def __init__(self):
        # Result
        self._mean = None

        self._data = None

    
    # Getters and setters
    @property
    def mean(self):
        return self._mean

    @mean.setter
    def mean(self, mean):
        self._mean = mean

    def get(self):
        return {"data": "Mean API working..."}

    def post(self):
        # Verify the datatype of the request body
        args = mean_post_args.parse_args()

        # Get the data
        data = args["data"]

        try:
            data = [float(number) for number in data.split(",")]

            self._data = data

            # Start the calculator
            calculator = Calculator(self._data)

            self._mean = calculator.mean()
            
            # Create the JSON response
            json_response = {
                "mean": self._mean
            }

            return json_response, 200
        except:
            # Create the JSON response
            json_response = {
                "mean": "Your data is not well structured, remember you must have an array of only numbers"
            }

            return json_response, 500
