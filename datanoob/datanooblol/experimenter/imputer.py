import numpy as np
import pandas as pd
import datanooblol.utils.calculator as cal
# from datanooblol.experimenter.base_fit_transform import BaseFitTransform
from datanooblol.utils.base import BaseFitTransform

class BaseImputer(BaseFitTransform):
    
    def __init__(self, imputed_feature:str):
        super().__init__()
        self.imputed_value = None
        self.imputed_feature = imputed_feature
        self.statistics = {"mean":cal._mean, "median":cal._median, "mode":cal._mode, 
                           "min":cal._min, "max":cal._max}

class SimpleImputer(BaseImputer):
    def __init__(self, imputed_feature:str, imputed_value):
        super().__init__(imputed_feature=imputed_feature)
        self.imputed_value = imputed_value
        
    def _transform(self, X):
        proxy = X.copy()
        proxy[self.imputed_feature].fillna(self.imputed_value, inplace=True)
        return proxy
    
class StatisticsImputer(BaseImputer):
    def __init__(self, imputed_feature:str, statistics:str, round_n=4):
        super().__init__(imputed_feature=imputed_feature)
        self.statistics = self.statistics[statistics]
        self.round_n = round_n
        
    def _fit(self, X):
        self.imputed_value = self.statistics(X[self.imputed_feature])
        
    def _transform(self, X):
        proxy = X.copy()
        if not isinstance(self.imputed_value, str):
            self.imputed_value = round(self.imputed_value, self.round_n)
        proxy[self.imputed_feature].fillna(self.imputed_value, inplace=True)
        return proxy
    
class GroupImputer(BaseImputer):
    def __init__(self, group_features:list[str], imputed_feature:str, statistics:str="mean"):
        super().__init__(imputed_feature=imputed_feature)
        self.group_features = group_features
        self.statistics = self.statistics[statistics]
        
    def _fit(self, X):
        self.imputed_value = X.groupby(self.group_features).agg({self.imputed_feature:self.statistics}).reset_index()
    
    def _transform(self, X):
        proxy = X.copy()
        for idx in range(self.imputed_value.shape[0]):
            mask = True
            for feature in self.group_features:
                mask = mask & (proxy[feature]==self.imputed_value.loc[idx, feature])
            mask = mask & (proxy[self.imputed_feature].isna())
            proxy.loc[mask, self.imputed_feature] = self.imputed_value.loc[idx, self.imputed_feature]
        
        return proxy