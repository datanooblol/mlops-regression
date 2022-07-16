from google.protobuf.duration_pb2 import Duration
from feast import Entity, Feature, FeatureView, FileSource, ValueType

# Declaring an entity for the dataset
house = Entity(name="house_id", value_type=ValueType.INT64, description="house_id",)

toxic_monthly_stats = FileSource(
    # path=f"{repo_path}/toxic.parquet",
    path="/usr/src/datanoob/repository/feature_store/toxic.parquet",
    event_timestamp_column="event_timestamp",
)

toxic_monthly_stats_view = FeatureView(
    name="toxic_monthly_stats",
    entities=["house_id"],
    # ttl=timedelta(seconds=86400 * 1),
    ttl=Duration(seconds=86400 * 3),
    features=[
        Feature(name="NOX", dtype=ValueType.FLOAT),
    ],
    batch_source=toxic_monthly_stats,
)

# Declaring the source of the targets
target_source = FileSource(
    path="/usr/src/datanoob/repository/feature_store/target.parquet", 
    created_timestamp_column="event_timestamp")

# Defining the targets
target_fv = FeatureView(
    name="target_feature_view",
    entities=["house_id"],
    ttl=Duration(seconds=86400 * 3),
    features=[
        Feature(name="MEDV", dtype=ValueType.FLOAT)        
        ],    
    batch_source=target_source
)