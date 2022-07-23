import pandas as pd
from datanooblol.extractor.data_extractor import DataExtractor
from datanooblol.extractor.reference_extractor import ReferenceExtractor
from sklearn.model_selection import train_test_split
from datanooblol.configuration.config_manager import LoadFeatureConfig, LoadRepoConfig

class ScopeData(ReferenceExtractor):
    def __init__(self, test_size:float=0.3, random_state:int=55, stratify:bool=False,
                X_feat_grp:list[str]=None, y_feat_grp:list[str]=None):
        # self.ref_xtr = ReferenceExtractor()
        super().__init__()
        self.repo_cfg = LoadRepoConfig()
        self.feat_cfg = LoadFeatureConfig()
        self.test_size = test_size
        self.random_state = random_state
        self.stratify = stratify
        self.X_feat_grp = ["entity"] + X_feat_grp
        self.y_feat_grp = ["entity"] + y_feat_grp
    
    def _get_features(self, xy_list:list[str]=None) -> list[str]:
        feat_list = []
        for grp in xy_list:
            for k, v in self.feat_cfg._get_config()[self.feat_cfg.param].items():
                if k == grp:
                     feat_list.append(list(v.keys()))

        return [feat for subset in feat_list for feat in subset]
    
    @property
    def _get_x(self):
        return self._get_features(xy_list=self.X_feat_grp)
    @property
    def _get_y(self):
        return self._get_features(xy_list=self.y_feat_grp)
        
    
    @property
    def split_data(self) -> dict:
        ref_data = self.extract_reference_data
        X = ref_data[self._get_x]
        y = ref_data[self._get_y]
        check_stratify = lambda x: None if self.stratify == False else x

        X_train, X_val, y_train, y_val = train_test_split(X, y,
                                                            test_size=self.test_size,
                                                            random_state=self.random_state, 
                                                            stratify=check_stratify(y))
        X_val, X_test, y_val, y_test = train_test_split(X_val, y_val,
                                                            test_size=0.5,
                                                            random_state=self.random_state, 
                                                            stratify=check_stratify(y_val))
        data_dict = {
            "X_train":X_train, "y_train":y_train,
            "X_val":X_val, "y_val":y_val,
            "X_test":X_test, "y_test":y_test
        }
        
        for method, data in data_dict.items():
            self._save_to_reference(method=method, data=data)
    
    def _save_to_reference(self, method:str, data:pd.DataFrame) -> None:
        data.to_parquet(f"{self.repo_cfg.REFERENCE_ZONE}/{method}.parquet")
    
    