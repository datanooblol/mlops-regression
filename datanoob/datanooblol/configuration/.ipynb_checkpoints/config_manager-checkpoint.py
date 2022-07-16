import yaml

class BaseConfig:
    def __init__(self):
        pass
    
    def _get_config(self) -> str:
        with open("../config/config.yaml", "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    
class LoadRepoConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.param = "data_repository"

    @property
    def DATA_SOURCE(self) -> str:
        return self._get_config()[self.param]["data_source"]
    
    @property
    def LANDING_ZONE(self) -> str:
        return self._get_config()[self.param]["landing"]
    
    @property
    def STAGING_ZONE(self) -> str:
        return self._get_config()[self.param]["staging"]    

    @property
    def FS_ZONE(self) -> str:
        return self._get_config()[self.param]["feature_store"]

    @property
    def PREDICTION_ZONE(self) -> str:
        return self._get_config()[self.param]["prediction"]

    @property
    def ARTIFACT_ZONE(self) -> str:
        return self._get_config()[self.param]["artifact"]

    @property
    def METADATA_ZONE(self) -> str:
        return self._get_config()[self.param]["metadata"]
    
    
class LoadFeatureConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.param = "features"
    
    def FEATURES(self, features: list[str]) -> str or list[str]:
        feature_list = []
        for feature in features:
            feature_list += self._get_config()[self.param][feature]
        
        if len(feature_list) == 1:
            return feature_list[0]
        else:
            return feature_list

class LoadScriptConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.param = "script"
    
    @property
    def PROJECT_INIT(self) -> str:
        return self._get_config()[self.param]["project_init"]
        
    @property
    def GENERATE_DOC(self) -> str:
        return self._get_config()[self.param]["generate_doc"]