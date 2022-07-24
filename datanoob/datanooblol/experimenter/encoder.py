from datanooblol.utils.base import BaseFitTransform
import importlib

class BinaryEncoder(BaseFitTransform):
    def __init__(self, encoded_features, value_map:dict):
        super().__init__()
        self.encoded_features = encoded_features
        self.value_map = value_map
        
    def _fit(self, X):
        pass
    
    def _transform(self, X):
        proxy = X.copy()
        proxy.loc[:,self.encoded_features] = proxy.loc[:, self.encoded_features].map(self.value_map)
        return proxy
    
class OneHotEncoder(BaseFitTransform):
    def __init__(self, encoded_features:list[str]):
        super().__init__()
        self.encoded_features = encoded_features
        self.encoder = importlib.import_module(f"sklearn.preprocessing").OneHotEncoder(sparse=False)
        
    def _fit(self, X):
        proxy = X.copy()
        self.encoder.fit(proxy.loc[:,self.encoded_features])
        
    def _transform(self, X):
        proxy = X.copy()
        proxy.loc[:,self.ohe.get_feature_names(self.encoded_features)] = self.encoder.transform(proxy.loc[:,self.encoded_features])
        return proxy
    
class LabelEncoder(BaseFitTransform):
    def __init__(self, encoded_features:list[str]):
        super().__init__()
        self.encoded_features = encoded_features
        self.encoder = importlib.import_module(f"sklearn.preprocessing").LabelEncoder()
        
    def _fit(self, X):
        proxy = X.copy()
        self.encoder.fit(proxy.loc[:, self.encoded_features])
        
    def _transform(self, X):
        proxy = X.copy()
        proxy.loc[:, self.encoded_features] = self.encoder.transform(proxy.loc[:,self.encoded_features])
        return proxy