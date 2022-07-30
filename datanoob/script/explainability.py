import importlib
import argparse

from datanooblol.serving.serving_manager import Serving
from datanooblol.extractor.reference_extractor import ReferenceExtractor
from shapash import SmartExplainer

import warnings
warnings.filterwarnings('ignore')

##############################################################################
# Create the parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('-p', '--project', help='project name', type=str, required=True)
parser.add_argument('-id', '--run_id', help='run_id from mlflow tracking', type=str, required=True)
# Parse the argument
args = parser.parse_args()
##############################################################################

def main(project, run_id):
    data = ReferenceExtractor(DEBUG=False)
    serving = Serving(project=project, run_id=run_id)
    loaded_exp, loaded_model = serving.get_serving_object
    X = data.X_test
    y = data.y_test
    
    xpl = SmartExplainer(model=loaded_model)
    xpl.compile(
        x=loaded_exp.X.transform(X),
        y_pred=loaded_exp.y.transform(y),
    )
    app = xpl.run_app(title_story=project)

if __name__ == "__main__":
    main(args.project, args.run_id)