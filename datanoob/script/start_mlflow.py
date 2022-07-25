import os
from datanooblol.configuration.config_manager import LoadModelTrackingConfig

if __name__ == "__main__":

    path = "/usr/src/datanoob/repository/metadata"

    db_path = "sqlite:///database/mlflow.db"
    art_path = "/usr/src/datanoob/repository/metadata/mlruns"

    backend = f"--backend-store-uri {db_path}"
    artifact = f"--default-artifact-root {art_path}"
    host = f"--host 0.0.0.0"
    port = f"--port 5000"

    command = f"cd {path} && mlflow server {backend} {artifact} {host} {port}"
    os.system(f"{command}")