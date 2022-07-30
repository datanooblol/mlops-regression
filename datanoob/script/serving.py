from datanooblol.serving.serving_manager import Serving
import argparse
from flask import Flask, request
import json
import pandas as pd

##############################################################################
# Create the parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('-p', '--project', help='project name', type=str, required=True)
parser.add_argument('-id', '--run_id', help='run_id from mlflow tracking', type=str, required=True)
parser.add_argument('-inv', '--inverse_y', help='inverse prediction value into the original', type=bool, required=True, default=False)
# Parse the argument
args = parser.parse_args()
##############################################################################

def dict_to_df(X:dict) -> pd.DataFrame:
    return pd.DataFrame(X, index=[0])

app = Flask(__name__)
@app.route('/predict', methods=["POST"])
def predict():
    # data = json.loads(request.get_json())
    X = request.get_json()
    X = dict_to_df(X)
    
    serving = Serving(project=args.project, run_id=args.run_id)
    prediction = serving.predict(X, inverse_y=args.inverse_y)
    response = {"prediction":list(prediction)}
    
    print("data", response)
    print("type", type(response))
    
    return json.dumps(response), 200

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=80)