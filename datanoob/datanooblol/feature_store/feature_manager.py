from feast import FeatureStore, Entity, FeatureView, Feature, ValueType, FileSource, RepoConfig, FeatureService, Field
from feast.types import PrimitiveFeastType
from feast.infra.offline_stores.file_source import SavedDatasetFileStorage
from datetime import datetime, timedelta
import pandas as pd
import os
from datanooblol.configuration.config_manager import LoadFeatureConfig, LoadRepoConfig, LoadFeatureStoreConfig, LoadFeastConfig
from feast.infra.offline_stores.file_source import SavedDatasetFileStorage


class FeatureStoreRegister:
    def __init__(self):
        self.fs_cfg = LoadFeatureStoreConfig()
        self.feat_cfg = LoadFeatureConfig()
        self.repo_cfg = LoadRepoConfig()
        self.feast_cfg = LoadFeastConfig()
        self.fs = FeatureStore(repo_path=self.fs_cfg.FS_REPO_CONFIG)
        self.entity = self.feat_cfg.ENTITY
        self.value_dict = {
            "float32":PrimitiveFeastType.FLOAT32, 
            "float64":PrimitiveFeastType.FLOAT64, 
            "int32":PrimitiveFeastType.INT32, 
            "int64":PrimitiveFeastType.INT64, 
            "str":PrimitiveFeastType.STRING, 
            "object":PrimitiveFeastType.STRING, 
            "bool": PrimitiveFeastType.BOOL, 
            "unix_timestamp": PrimitiveFeastType.UNIX_TIMESTAMP, 
            "bytes": PrimitiveFeastType.BYTES,
            "invalid": PrimitiveFeastType.INVALID
        }
        
    def _get_filesource(self, feature_grp:str):
        return FileSource(path=f"{self.repo_cfg.FS_ZONE}/{feature_grp}.parquet", timestamp_field=self.feat_cfg.FEATURES(features=["timestamp_field"]))
    
    def _get_fs_view(self, name:str=None, entities:list=None, schema:dict[str]=None, source=None):
        return FeatureView(
            name=name,
            entities=entities,
            ttl=timedelta(seconds=86400 * self.fs_cfg.TTL),
            schema=[Field(name=feature, dtype=self.value_dict[dtype]) for feature, dtype in schema.items()],
            source=source
        )
    def _register(self, feature_grp, schema):
        entity_name = list(self.entity.keys())[0]
        entity = Entity(name=entity_name, description=entity_name)
        source = self._get_filesource(feature_grp=feature_grp)
        view = self._get_fs_view(name=f"{feature_grp}", entities=[entity], schema=schema, source=source)
        self.fs.apply([entity, view])
    
    @property
    def register(self):
        for feature_grp, schema in self.feat_cfg.FEATURE_GROUP.items():
            schema.update(self.entity)
            self._register(feature_grp, schema)
    
    @property
    def _pair_grp_feature(self):
        feature_list = []
        for grp, features in self.feat_cfg.FEATURE_GROUP.items():
            for feature in features.keys():
                if grp != "target":
                    feature_list.append(f"{grp}:{feature}")
        return feature_list
    
    @property
    def create_dataset(self):
        entity_df = pd.read_parquet(path=f"{self.repo_cfg.FS_ZONE}/target.parquet")

        feature_list = self._pair_grp_feature
        training_data = self.fs.get_historical_features(
            entity_df=entity_df,
            features=feature_list,
        )
        dataset = self.fs.create_saved_dataset(
            from_=training_data,
            name=f"{self.feast_cfg.PROJECT_NAME}",
            storage=SavedDatasetFileStorage(f"{self.repo_cfg.REFERENCE_ZONE}/{self.feast_cfg.PROJECT_NAME}_dataset.parquet")
        )
    
    @property
    def materialize(self):
        self.fs.materialize(
            end_date=datetime.now(),
            start_date=datetime.now() - timedelta(days=self.fs_cfg.MATERIALIZE_DAY)
        )
    
    @property
    def materialize_incremental(self):
        self.fs.materialize_incremental(end_date=datetime.now())
        
        
    def get_online_features(self, entity_list_dict:list[dict]) -> pd.DataFrame:
        feature_list = self._pair_grp_feature
        features = self.fs.get_online_features(
            features=feature_list,
            entity_rows=entity_list_dict
        ).to_dict()
        return pd.DataFrame.from_dict(data=features)