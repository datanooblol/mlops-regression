# Importing dependencies
from feast import FeatureStore
import pandas as pd
from joblib import load

# Getting our FeatureStore
store = FeatureStore(repo_path="repository/")

# Defining our features names
feast_features = [
        "toxic_monthly_stats:NOX",
    ]

# Getting the latest features
features = store.get_online_features(
    features=feast_features,    
    entity_rows=[{"house_id": 345}, {"house_id": 344}]
).to_dict()

# Converting the features to a DataFrame
# features_df = pd.DataFrame.from_dict(data=features)

print(features)
# Loading our model and doing inference
# reg = load("model.joblib")
# predictions = reg.predict(features_df[sorted(features_df.drop("patient_id", axis=1))])