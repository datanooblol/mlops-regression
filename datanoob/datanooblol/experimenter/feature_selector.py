import pandas as pd
from datanooblol.configuration.config_manager import ExperimentConfig
from datanooblol.utils.base import BaseFitTransform

class BaseSelector(BaseFitTransform):
    
    def __init__(self,):
        super().__init__()
        self.features = None
        self.scaler = None
    
    def _fit(self, X):
        pass
    
    def _transform(self, X):
        proxy = X.copy()
        # proxy.loc[:, self.features] = self.scaler.transform(X.loc[:,self.features])
        proxy.loc[:, self.features] = proxy.loc[:, self.features]
        return self.to_frame(proxy)
    
    def to_frame(self, X):
        # features = self.features if len(self.features) > 1 else list(self.features)
        # return pd.DataFrame(X, columns=features)
        return pd.DataFrame(X, columns=self.features)

class FeatureSelector(BaseSelector):
    def __init__(self, features):
        super().__init__()
        self.features = features
            
class PassThrough(BaseSelector):
    def __init__(self, features):
        super().__init__()
        self.features = features
        
    def inverse_transform(self, X):
        return X
        