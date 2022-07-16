import pandas as pd
import numpy as np
import os
from datetime import timedelta
from datanooblol.configuration.config_manager import LoadRepoConfig, LoadFeatureConfig


def init_data():
    """
    Get .csv data and convert to .parquet and generate a datetime column
    
    """
    # print(os.getcwd()) # run this command to find your current working directory in case you cannot find a file path
    
    # load raw csv file
    repo_cfg = LoadRepoConfig()
    feat_cfg = LoadFeatureConfig()
    
    column_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
        
    df = pd.read_csv(f'{repo_cfg.DATA_SOURCE}/housing.csv', header=None, delimiter=r"\s+", names=column_names)
    row, col = df.shape

    # generate datetime
    init_date = (pd.Timestamp.now() + pd.DateOffset(months=-3)).strftime("%Y-%m")
    seq_1 = pd.to_datetime(f"{init_date} 00:00:00")
    seq_2 = seq_1 + pd.DateOffset(months=1)
    seq_3 = seq_1 + pd.DateOffset(months=2)
    seq_4 = seq_1 + pd.DateOffset(months=3)
    get_dt = lambda x: x.strftime("%Y-%m-%d")
    
    # initiate dataset
    
    df["event_timestamp"] = seq_1
    df["load_dt"] = get_dt(seq_1)
    df["house_id"] = np.arange(df.shape[0]) + 1
    
    
    # sample and add new record
    
    new_df = df.copy()
    sample_ratio = 0.5
    
    for seed, seq in enumerate([seq_2, seq_3, seq_4]):
        
        sample_df = df.sample(int(row*sample_ratio), random_state=seed)
        sample_df["event_timestamp"] = seq
        sample_df["load_dt"] = get_dt(seq)
        
        # change MEDV value
        np.random.seed(seed)
        sample_df["MEDV"] = sample_df["MEDV"] + np.random.randn()
        
        new_df = pd.concat([new_df, sample_df], axis=0)
        
    # save to parquet by feature group
    
    subset_features = lambda x: feat_cfg.FEATURES(["entity", "event_timestamp", "load_date", x])
    feature_list = ["proportion", "geography", "toxic", "monetary", "target"]

    for feature in feature_list:
        new_df[subset_features(feature)].to_parquet(
            path=f"{repo_cfg.LANDING_ZONE}/{feature}",
            engine="pyarrow",
            compression="snappy",
            partition_cols=["load_dt"],
            index=False
        )
