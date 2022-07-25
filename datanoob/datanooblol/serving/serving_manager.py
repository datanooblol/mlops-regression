import mlflow
import pickle
from datanooblol.configuration.config_manager import LoadModelTrackingConfig


class Serving:
    """
    Serving class is used for deployment and production phase. It extracts experiment and model objects based on model run_id of MLflow tracking
    
    """
    def __init__(self, project:str, run_id:str):
        self.project = project
        self.run_id = run_id
        self.tracking_cfg = LoadModelTrackingConfig()
        mlflow.set_tracking_uri(self.tracking_cfg.TRACKING_URI)
    
    @property
    def get_serving_object(self) -> tuple:
        model_path = mlflow.search_runs(experiment_names=[self.project], 
                                        filter_string=f"tags.run_id='{self.run_id}'")["artifact_uri"].values[0]
        filename = f"{model_path}/model/model.pkl"

        experiment = pickle.load(open(f"{model_path}/experiment/experiment.pkl", 'rb'))
        model = pickle.load(open(f"{model_path}/model/model.pkl", 'rb'))
        return experiment, model
    
    def predict(self, X):
        loaded_exp, loaded_model = self.get_serving_object
        return loaded_model.predict(loaded_exp.X.transform(X))