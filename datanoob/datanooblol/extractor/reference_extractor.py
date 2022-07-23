import pandas as pd
from datanooblol.configuration.config_manager import LoadFeatureConfig, LoadRepoConfig, LoadFeastConfig, LoadFeatureConfig
from datanooblol.extractor.data_extractor import DataExtractor

class ReferenceExtractor:
    def __init__(self, DEBUG=False):
        self.DEBUG = DEBUG
        self.feast_cfg = LoadFeastConfig()
        self.repo_cfg = LoadRepoConfig()
        self.feat_cfg = LoadFeatureConfig()
    @property
    def extract_reference_data(self):
        return pd.read_parquet(f"{self.repo_cfg.REFERENCE_ZONE}/{self.feast_cfg.PROJECT_NAME}_dataset.parquet")
    
    def _extract(self, method:str)->pd.DataFrame:
        if self.DEBUG == True:
            return pd.read_parquet(f"{self.repo_cfg.REFERENCE_ZONE}/{method}.parquet")
        else:
            return pd.read_parquet(f"{self.repo_cfg.REFERENCE_ZONE}/{method}.parquet").drop(self.feat_cfg.ENTITY, axis=1)
        
    @property
    def X_train(self):
        return self._extract(method="X_train")
    
    @property
    def X_val(self):
        return self._extract(method="X_val")
    
    @property
    def X_test(self):
        return self._extract(method="X_test")
    
    @property
    def y_train(self):
        return self._extract(method="y_train")
    
    @property
    def y_val(self):
        return self._extract(method="y_val")
    
    @property
    def y_test(self):
        return self._extract(method="y_test")