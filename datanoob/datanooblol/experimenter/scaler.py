# test and pass

import numpy as np
import pandas as pd
from datanooblol.utils.base import BaseFitTransform
from sklearn.preprocessing import MinMaxScaler, PowerTransformer, StandardScaler
from datanooblol.configuration.config_manager import ExperimentConfig

class Scaler(BaseFitTransform):
    
    def __init__(self, scaled_features, scaler):
        super().__init__()
        self.scaled_features = scaled_features
        self.scaler = {"min_max":MinMaxScaler(), "z_scale":StandardScaler(), 
                       "yeo_johnson":PowerTransformer(method="yeo-johnson"), 
                       "box_cox":PowerTransformer(method="box-cox")}[scaler]
    
    def _fit(self, X):
        self.scaler.fit(X.loc[:, self.scaled_features])
    
    def _transform(self, X):
        proxy = X.copy()
        proxy.loc[:, self.scaled_features] = self.scaler.transform(X.loc[:,self.scaled_features])
        return proxy
    
    def fit_transform(self, X):
        return self.fit(X).transform(X)
    
class BaseScaler(BaseFitTransform):
    
    def __init__(self,):
        super().__init__()
        self.features = None
        self.scaler = None
    
    def _fit(self, X):
        self.scaler.fit(X.loc[:, self.features])
    
    def _transform(self, X):
        proxy = X.copy()
        proxy.loc[:, self.features] = self.scaler.transform(X.loc[:,self.features])
        return self.to_frame(proxy)
    
    def to_frame(self, X):
        # features = self.features if len(self.features) > 1 else list(self.features)
        # return pd.DataFrame(X, columns=features)
        return pd.DataFrame(X, columns=self.features)
    
class ZScaler(BaseScaler):
    def __init__(self, features:list[str]):
        super().__init__()
        self.features = features
        self.scaler = StandardScaler()
        
class MMScaler(BaseScaler):
    def __init__(self, features:list[str]):
        super().__init__()
        self.features = features
        self.scaler = MinMaxScaler()
        
class YeoJohnsonScaler(BaseScaler):
    def __init__(self, features:list[str]):
        super().__init__()
        self.features = features
        self.scaler = PowerTransformer(method="yeo-johnson")
        
class BoxCoxScaler(BaseScaler):
    def __init__(self, features:list[str]):
        super().__init__()
        self.features = features
        self.scaler = PowerTransformer(method="box-cox")