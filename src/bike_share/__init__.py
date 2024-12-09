from dagster import Definitions

from bike_share.config import (
    DATA_DIRECTORY,
    MLFLOW_EXPERIMENT,
    MLFLOW_TRACKING_URL,
    XBG_LEARNING_RATE,
    XBG_MAX_DEPTH,
    XGB_COLSAMPLE_BYTREE,
    XGB_N_ESTIMATORS,
    XGB_SUBSAMPLE,
)
from bike_share.resources.data_loader import DataLoader
from bike_share.resources.mlflow_session import MlflowSession

definitions = Definitions(
    assets=[],
    resources={
        "data_loader": DataLoader(
            data_directory=DATA_DIRECTORY,
        ),
        "mlflow_session": MlflowSession(
            tracking_url=MLFLOW_TRACKING_URL,
            experiment=MLFLOW_EXPERIMENT,
        ),
    },
)
