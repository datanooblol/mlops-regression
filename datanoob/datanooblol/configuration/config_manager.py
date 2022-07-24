import yaml

class BaseConfig:
    def __init__(self):
        self.config_path = "../config/config.yaml"
    
    def _get_config(self) -> str:
        with open(self.config_path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        return config
    
class LoadRepoConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.param = "data_repository"

    @property
    def REPOSITORY(self) -> str:
        return self._get_config()[self.param]["repository"]
        
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
    
    @property
    def REFERENCE_ZONE(self) -> str:
        return self._get_config()[self.param]["reference"]
    
    @property
    def DATABASE_ZONE(self) -> str:
        return self._get_config()[self.param]["database"]
    
    @property
    def EXPERIMENT_ZONE(self) -> str:
        return self._get_config()[self.param]["experiment"]
    
class LoadFeatureStoreConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.param = "feature_store_config"
        
    @property
    def FS_REPO_CONFIG(self) -> str:
        return self._get_config()[self.param]["fs_repo_config"]
    
    @property
    def TTL(self):
        return self._get_config()[self.param]["ttl"]
    
    @property
    def MATERIALIZE_DAY(self):
        return self._get_config()[self.param]["materialize_day"]
        # return self._get_config()[self.param]
    @property
    def CONFIG(self):
        # return self._get_config()[self.param]["materialize_day"]
        return self._get_config()[self.param]
    
class LoadFeastConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.config_path = "../config/feature_store.yaml"
        # self.param = "feature_store_config"
        
    @property
    def PROJECT_NAME(self):
        return self._get_config()["project"]
    
class LoadFeatureConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.config_path = "../config/feature_group.yaml"
        self.param = "feature_group"
    
    def FEATURES(self, features: list[str]) -> str or list[str]:
        feature_list = []
        for feature in features:
            feature_list += self._get_config()[self.param][feature].keys()
        
        if len(feature_list) == 1:
            return feature_list[0]
        else:
            return feature_list

        
    @property
    def FEATURE_GROUP(self) -> dict:
        feature_groups = self._get_config()[self.param]
        filter_out = ["entity", "timestamp_field", "load_date"]
        return {feat_grp:dtype for feat_grp, dtype in feature_groups.items() if feat_grp not in filter_out}
    
    @property
    def ENTITY(self) -> str:
        return self._get_config()[self.param]["entity"]

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
    
class LoadExpConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        
class LoadModelTrackingConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.param = "model_tracking"
        
    @property
    def TRACKING_URI(self):
        return self._get_config()[self.param]["tracking_uri"]
    
    @property
    def MLRUN_PATH(self):
        return self._get_config()[self.param]["mlrun_path"]
    
class EDAConfig(BaseConfig):
    def __init__(self):
        super().__init__()
        self.param = "eda"
        
    @property
    def HOST(self):
        return self._get_config()[self.param]["host"]
    
    @property
    def PORT(self):
        return self._get_config()[self.param]["port"]
    
class ExperimentConfig(BaseConfig):
    def __init__(self, experiment_file:str, Xy:str=None):
        super().__init__()
        # self.config_path = f"../repository/metadata/experiment/{experiment_file}"
        self.config_path = experiment_file
        self.param = Xy
    
    @property
    def Xy_CONFIG(self):
        return self._get_config()[self.param]
    
    # @property
    # def MODEL_AVILABLE(self):
    #     return self._get_config()["model"]
    @property
    def PROJECT(self):
        return self._get_config()["project"]
    
    @property
    def OBJECTIVE(self):
        return self._get_config()["objective"]
    
    @property
    def STAGE(self):
        return self._get_config()["stage"]
    
    @property
    def DESC(self):
        return self._get_config()["experiment_desc"]

class ModelConfig(BaseConfig):
    def __init__(self, experiment_file:str):
        super().__init__()
        # self.config_path = f"../repository/metadata/experiment/{experiment_file}"
        self.config_path = experiment_file
        self.param = "model"
    
    @property
    def EXPERIMENT_MODEL(self):
        return self._get_config()[self.param]