import numpy as np
import pandas as pd
from datanooblol.utils.base import BaseFitTransform
from sklearn.preprocessing import MinMaxScaler, PowerTransformer, StandardScaler

class Scaler(BaseFitTransform):
    
    def __init__(self, scaled_features, scaler):
        super().__init__()
        self.scaled_features = scaled_features
        self.scaler = {"min-max":MinMaxScaler(), "standard":StandardScaler(), 
                       "yeo-johnson":PowerTransformer(method="yeo-johnson"), 
                       "box-cox":PowerTransformer(method="box-cox")}[scaler]
    
    def _fit(self, X):
        self.scaler.fit(X.loc[:, self.scaled_features])
    
    def _transform(self, X):
        proxy = X.copy()
        proxy.loc[:, self.scaled_features] = self.scaler.transform(X.loc[:,self.scaled_features])
        return proxy
    
    def fit_transform(self, X):
        return self.fit(X).transform(X)