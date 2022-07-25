import pandas as pd
import os
from datanooblol.configuration.config_manager import LoadFeatureConfig, LoadRepoConfig

class DataUploader:
    """
    Upload data into a zone and stage based on input parameters
    
    """
    def __init__(self):
        self.feat_cfg = LoadFeatureConfig()
        self.repo_cfg = LoadRepoConfig()
        self.zone = {
            "landing": self.repo_cfg.LANDING_ZONE,
            "staging": self.repo_cfg.STAGING_ZONE,
            "feature_store": self.repo_cfg.FS_ZONE,
        }
        
    def upload_zone(self, zone:str=None, step:str=None, feature_grp:str=None, data:pd.DataFrame=None) -> None:
        self._upload(zone=zone, step=step, feature_grp=feature_grp, data=data)
    
    def _upload(self, zone:str, step:str, feature_grp:str, data:pd.DataFrame) -> None:
        repo_path = self.zone[zone]
        if step != None:
            repo_path = f"{repo_path}/{step}"
        data.to_parquet(f"{repo_path}/{feature_grp}",
                        engine="pyarrow", 
                        compression="snappy",
                        partition_cols=[self.feat_cfg.FEATURES(["load_date"])],
                        index=False)
        
    def upload_feature_store(self, feature_grp:str, data: pd.DataFrame) -> None:
        """
        Upload final data to feature store as a single file
        
        :param str feature_grp: feature group name
        :param pd.DataFrame data: data to be uploaded
        :returns: None
        :rtype: None
        """
        repo_path = self.repo_cfg.FS_ZONE
        data.to_parquet(f"{repo_path}/{feature_grp}.parquet",
                       engine="pyarrow",
                       compression="snappy",
                       index=False)

        
        
        
    