import pandas as pd
from datanooblol.configuration.config_manager import ExperimentConfig
from datanooblol.utils.base import BaseFitTransform
from datanooblol.experimenter.feature_selector import FeatureSelector
from datanooblol.experimenter.experiment_catalogue import ExperimentCatalogue
from functools import reduce

class ExperimentGenerator(BaseFitTransform):
    """
    Pack necessary transform tasks into one single object
    
    :param str experiment_file: path for a selected experiment
    :param str Xy: select X or y tasks
    :return: pd.DataFrame in transform or fit_transform method
    :rtype: pd.DataFrame
    """
    def __init__(self, experiment_file:str, Xy:str):
        super().__init__()
        self.experiment_file = experiment_file
        self.exp_catalogue = ExperimentCatalogue()
        self.exp_cfg = ExperimentConfig(experiment_file=self.experiment_file, Xy=Xy).Xy_CONFIG
        self.tasks = {}
        self._pack_tasks
    
    def _get_task(self, task_name):
        """
        return experiment object
        """
        return self.exp_catalogue.get_experiment_task(task_name)
    
    @property
    def _pack_tasks(self):
        """
        pack dictionary
        """
        for task_name in self.exp_cfg.keys():
            if task_name in ["ZScaler", "MMScaler", "YeoJohnsonScaler", "BoxCoxScaler"]:
                task = self._get_task(task_name)(features=self.exp_cfg[task_name])
            # elif task_name in ["OneHotEncoder", "LabelEncoder"]:
            #     task = self._get_task(task_name)(encoded_features=self.exp_cfg[task_name])
            # elif task_name in ["BinaryEncoder"]:
            #     task = self._get_task(task_name)(encoded_features=[], value_map={})
            elif task_name in ["PassThrough"]:
                task = self._get_task(task_name)(features=self.exp_cfg[task_name])
            else:
                raise Exception(f"task invalid: {task_name} is not in experiment_catalogue. Please check experiment_catalogue.py for available tasks")
            
            if task_name != "FeatureSelector":
                self.tasks.update({task_name:task})
    
    def _fit(self, X):
        for task_name in self.tasks.keys():
            self.tasks[task_name].fit(X)
    
    def _transform(self, X):
        proxy = reduce(lambda  left, right: pd.concat([left, right], axis=1), [task.transform(X) for task in self.tasks.values()])
        if "FeatureSelector" in self.exp_cfg.keys():
            proxy = proxy.loc[:, self.exp_cfg["FeatureSelector"]].copy()
        return proxy
        
class ExperimentPackage:
    def __init__(self, experiment_file):
        self.X = ExperimentGenerator(experiment_file=experiment_file, Xy="X")
        self.y = ExperimentGenerator(experiment_file=experiment_file, Xy="y")