# test and pass

import importlib
import argparse

from datanooblol.extractor.reference_extractor import ReferenceExtractor
from datanooblol.experimenter.experiment_generator import ExperimentGenerator, ExperimentPackage
from datanooblol.modeling.model_generator import ModelGenerator
from datanooblol.modeling.trainer import Trainer
from datanooblol.configuration.config_manager import LoadRepoConfig, ExperimentConfig

import warnings
warnings.filterwarnings('ignore')

##############################################################################
# Create the parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--experiment_name', type=str, required=True)
# Parse the argument
args = parser.parse_args()
##############################################################################

if __name__=="__main__":

##############################################################################
    experiment_path = LoadRepoConfig().EXPERIMENT_ZONE
    experiment_name = args.experiment_name
    experiment_file = f"{experiment_path}/{experiment_name}.yaml"
    experiment = ExperimentPackage(experiment_file=experiment_file)
    exp_cfg = ExperimentConfig(experiment_file=experiment_file)
##############################################################################
    project = exp_cfg.PROJECT
    objective = exp_cfg.OBJECTIVE
    stage = exp_cfg.STAGE
    proj_desc = exp_cfg.DESC
##############################################################################    
    data = ReferenceExtractor(DEBUG=False)
    X_train = experiment.X.fit_transform(data.X_train)
    y_train = experiment.y.fit_transform(data.y_train)
    X_val = experiment.X.transform(data.X_val)
    y_val = experiment.y.fit_transform(data.y_val)
    X_test = experiment.X.transform(data.X_test)
    y_test = experiment.y.fit_transform(data.y_test)
##############################################################################
    models = ModelGenerator(experiment_file=experiment_file).models
##############################################################################    
    trainer = Trainer(project=project, 
                      experiment_name=experiment_name, 
                      objective=objective,
                      stage=stage,
                      experiment=experiment, 
                      models=models)

    trainer.fit(X_train, y_train, X_test, y_test)
    print(f"{len(models)} models: trained successfully")