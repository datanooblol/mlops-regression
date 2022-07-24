from importlib import import_module

class ExperimentCatalogue:
    def __init__(self):
        self.experiment_path = "datanooblol.experimenter"
        self.experiment_catalogue = {
            "SimpleImputer": f"{self.experiment_path}.imputer",
            "StatisticImputer": f"{self.experiment_path}.imputer",
            "GroupImputer": f"{self.experiment_path}.imputer",
            "BinaryEncoder": f"{self.experiment_path}.encoder",
            "OneHotEncoder": f"{self.experiment_path}.encoder",
            "LabelEncoder": f"{self.experiment_path}.encoder",
            "MMScaler": f"{self.experiment_path}.scaler",
            "ZScaler": f"{self.experiment_path}.scaler",
            "YeoJohnsonScaler": f"{self.experiment_path}.scaler",
            "BoxCoxScaler": f"{self.experiment_path}.scaler",
            "PassThrough": f"{self.experiment_path}.feature_selector",
            "FeatureSelector": f"{self.experiment_path}.feature_selector",
        }
    
    
    def get_experiment_task(self, task_name):
        task_path = self.experiment_catalogue[task_name]
        return getattr(import_module(f"{task_path}"), f"{task_name}")