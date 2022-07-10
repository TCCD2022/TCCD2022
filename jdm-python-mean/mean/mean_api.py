from flask_restful import Resource, reqparse, abort, request
import sys
sys.path.append("..")
from utils.calculator import Calculator

# Config the required parameters for the api method
mean_put_args = reqparse.RequestParser()
mean_put_args.add_argument("data", type=str, help="Data array is required", required=True)

class MeanApi(Resource):
    def __init__(self):
        # Result
        self._mean = None

        self._data = None

        # Start the calculator
        self._calculator = Calculator()

    
    # Getters and setters
    @property
    def mean(self):
        return self._mean

    @mean.setter
    def mean(self, mean):
        self._mean = mean

    @property
    def calculator(self):
        return self._calculator

    @calculator.setter
    def calculator(self, calculator):
        self._calculator = calculator


    # HTTP methods
    def get(self):
        return {"data": "Mean API working..."}

    def put(self):
        # Verify the datatype of the request body
        args = mean_put_args.parse_args()

        

        # Get the data
        data = args["data"]

        print(data)

        try:
            data = [float(number) for number in data.split(",")]

            self._data = data

            self._mean = self._calculator.mean_put(data)
            
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

    def post(self):
        # Verify the datatype of the request body
        # args = mean_post_args.parse_args()
        request_data = request.get_json()

        if ('data' in request_data):
            # Get the data
            data = request_data["data"]

            try:
                data = [float(number) for number in data.split(",")]

                print(data)
            
                mean = self._calculator.basic_mean()
                
                # Create the JSON response
                json_response = {
                    "mean": mean
                }

                return json_response, 200
            except:
                # Create the JSON response
                json_response = {
                    "mean": "Your data is not well structured, remember you must have an array of only numbers"
                }
        else:
           self._calculator.mean(request_data); 


