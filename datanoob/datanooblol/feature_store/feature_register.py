from datanooblol.configuration.config_manager import LoadFeatureConfig
import pandas as pd
import os
import yaml

class FeatureRegister:
    def __init__(self):
        self.config_path = "../config/feature_group.yaml"
    
    def _get_config(self) -> str:
        if not os.path.exists(self.config_path):
            os.system(f"touch {self.config_path}")
        with open(self.config_path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    
    def _register(self, feature_grp, feature_dtype):
        config_dict = self._get_config()
        if config_dict == None:
            # config_dict = dict(feature_grp=feature_grp)
            config_dict = {
                "feature_group": {feature_grp:feature_dtype}
            }
        else:
            config_dict["feature_group"].update({feature_grp:feature_dtype})
        with open(self.config_path, "w") as f:
            config = yaml.dump(config_dict, f)
        
        return config_dict
    
    def _pair_feat_dtype(self, features:list[str], data:pd.DataFrame) -> dict[str]:
        return {feature:str(data[feature].dtype) for feature in features}
    
    def register(self, feature_grp:str, features, data) -> None:
        feature_dtype = self._pair_feat_dtype(features=features, data=data)
        self._register(feature_grp=feature_grp, feature_dtype=feature_dtype)