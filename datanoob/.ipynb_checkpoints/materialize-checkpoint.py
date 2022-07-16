# Importing dependencies
from feast import FeatureStore
from datetime import datetime, timedelta

# Getting our FeatureStore
fs = FeatureStore(repo_path="repository/")

# Code for loading features to online store between two dates
"""store.materialize(
    end_date=datetime.now(),
    start_date=datetime.now() - timedelta(days=700))"""

# Loading the latest features after a previous materialize call or from the beginning of time
fs.materialize_incremental(end_date=datetime.now())