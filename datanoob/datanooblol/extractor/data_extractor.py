import pandas as pd
import os
from datanooblol.configuration.config_manager import LoadFeatureConfig, LoadRepoConfig, LoadFeastConfig


class DataExtractor:
    """
    Extract data from each zone
    
    :param str end_date: end date
    :param str start_date: start date
    """
    def __init__(self, end_date:str = None, start_date:str = None, partition:str = None):
        self.feat_cfg = LoadFeatureConfig()
        self.feast_cfg = LoadFeastConfig()
        self.repo_cfg = LoadRepoConfig()
        self.zone = {
            "landing": self.repo_cfg.LANDING_ZONE,
            "staging": self.repo_cfg.STAGING_ZONE,
            "feature_store": self.repo_cfg.FS_ZONE,
            "reference": self.repo_cfg.REFERENCE_ZONE,
        }
        self.end_date = end_date
        self.start_date = start_date
        self.partition = partition
    
    def _logic_date_range(self, date_range:list[str]) -> list[str]:
        if (self.end_date == None) & (self.start_date == None):
            return date_range
        elif (self.end_date != None) & (self.start_date == None):
            date_range = date_range[(date_range <= self.end_date)]
            return date_range
        elif (self.end_date == None) & (self.start_date != None):
            date_range = date_range[(date_range >= self.start_date)]
            return date_range
        else:
            date_range = date_range[(date_range < self.start_date)==(date_range > self.end_date)]
            return date_range
        
    def _get_date_range(self, repo_path:str, feature_grp:str) -> list[str]:
        
        date_range = pd.Series([repo.split("=")[-1] for repo in os.listdir(f"{repo_path}/{feature_grp}")])
        date_list = self._logic_date_range(date_range=date_range)
        return date_list
    
    def _extract(self, repo_path:str, step:str , feature_grp:str, partition:str) -> pd.DataFrame:        

        if step != None:
            repo_path = f"{repo_path}/{step}"
        
        partition_list = self._get_date_range(repo_path=repo_path, 
                                         feature_grp=feature_grp)
        
        df = pd.read_parquet(f"{repo_path}/{feature_grp}", 
                             engine="pyarrow", 
                             filters=[
                                 (self.partition, 'in', partition_list)
                             ])
        df[self.partition] = df[self.partition].astype("object")
        return df
    
    def extract_zone(self, zone:str=None, step:str=None, feature_grp:str=None,
                    partition:str=None) -> pd.DataFrame:
        """
        Extract feature group based on a selected zone and return dataframe
        
        :param str zone: extract based on zone - optional argument - [landing, staging, feature_store]
        :param str step: extract based on step and used exculsively with staging area - default = None - optional argument - [None, cleaned, aggregated, joined]
        :param str feature_grp: name of feature group
        :returns: pandas dataframe
        :rtype: pd.DataFrame        
        """
        return self._extract(repo_path=self.zone[zone], step=step, feature_grp=feature_grp, partition=partition)
        
    
#     def extract_landing(self, feature_grp: str) -> pd.DataFrame:
#         """
#         Extract feature group from landing zone and return dataframe
        
#         :param str feature_grp: name of feature group
#         :returns: pandas dataframe
#         :rtype: pd.DataFrame        
#         """
#         return self._extract(repo_path=self.zone["landing"], feature_grp=feature_grp)
    
#     def extract_staging(self, feature_grp: str) -> pd.DataFrame:
#         """
#         Extract feature group from staging zone and return dataframe
        
#         :param str feature_grp: name of feature group
#         :returns: pandas dataframe
#         :rtype: pd.DataFrame        
#         """
#         return self._extract(repo_path=self.zone["staging"], feature_grp=feature_grp