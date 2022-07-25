import mlflow
import os
import pickle
# import timeit
import importlib
from tqdm import tqdm
from datanooblol.configuration.config_manager import LoadModelTrackingConfig

class Trainer:
    """
    A wrapper class for training model and tracking all neccesary artifacts into MLFlow
    
    """
    def __init__(self, project:str, experiment_name:str, objective:str, stage:str, experiment, models:list):
        self.project = project
        self.experiment_name = experiment_name
        self.objective = objective
        self.evaluator_path = f"datanooblol.evaluator.{objective}_evaluator"
        self.stage = stage
        self.experiment = experiment
        self.models = models
        self.tracking_cfg = LoadModelTrackingConfig()
        mlflow.set_tracking_uri(self.tracking_cfg.TRACKING_URI)

    def _fit_tracking(self, model_name, model, param,
                     X_train, y_train, X_test, y_test):
        experiment_id = mlflow.set_experiment(self.project).experiment_id
        with mlflow.start_run(run_name=model_name,
                             experiment_id=experiment_id) as run:
            run_id = run.info.run_id
            experiment_path = f"{self.tracking_cfg.MLRUN_PATH}/{experiment_id}/{run_id}/artifacts/experiment"
            tags = {
                "experiment": self.experiment_name,
                "model_name": model_name,
                "stage":self.stage,
                "feature_n": X_train.shape[1],
                "run_id": run_id,
            }
            mlflow.set_tags(tags)
            model.fit(X_train, y_train.to_numpy().reshape(-1))
            evaluator = importlib.import_module(f"{self.evaluator_path}").Evaluator()
            evaluation_dict = evaluator.evaluate(model=model, X=X_test, y_actual=y_test)

            mlflow.log_metrics(evaluation_dict)
            mlflow.log_params(param)
            mlflow.sklearn.log_model(model, artifact_path="model")
            if not os.path.exists(experiment_path):
                os.mkdir(experiment_path)
            with open(f"{experiment_path}/experiment.pkl", "wb") as f:
                pickle.dump(self.experiment, f)

    def fit(self, X_train, y_train, X_test, y_test):
        # mlflow.set_tracking_uri(self.tracking_cfg.TRACKING_URI)
        # for model_name, model, param in self.models:
        for model_name, model, param in tqdm(self.models, desc="Training..."):
            self._fit_tracking(model_name, model, param, 
                               X_train, y_train, X_test, y_test)
