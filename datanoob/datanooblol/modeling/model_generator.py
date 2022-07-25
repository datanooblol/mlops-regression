import pandas as pd
from datanooblol.configuration.config_manager import ExperimentConfig, ModelConfig
from datanooblol.utils.base import BaseFitTransform
from datanooblol.modeling.model_catalogue import ModelCatalogue
from datanooblol.modeling.model_builder import ModelBuilder
from functools import reduce

class ModelGenerator():
    """
    Generate a list of models based on a selected experiment.yaml
    
    """
    def __init__(self, experiment_file:str):
        super().__init__()
        self.experiment_file = experiment_file
        self.model_catalogue = ModelCatalogue()
        self.model_cfg = ModelConfig(experiment_file=self.experiment_file).EXPERIMENT_MODEL
        self.model_builder = ModelBuilder()
        self.models = []
        self._pack_models
    
    def _get_model(self, model_name, parameters) -> list:
        """
        return model object
        """
        model=self.model_catalogue.get_model(model_name)
        
        return self.model_builder.build(model_name=model_name, model=model, parameters=parameters)
    
    @property
    def _pack_models(self) -> list:
        """
        pack list
        """
        for model_name, parameters in self.model_cfg.items():
            self.models += self._get_model(model_name, parameters)