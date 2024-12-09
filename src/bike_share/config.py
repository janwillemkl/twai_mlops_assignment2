DATA_DIRECTORY = "data"

NUMERIC_FEATURES = [
    "temp",
    "hum",
    "windspeed",
    "cnt_lag_1",
    "cnt_lag_2",
    "cnt_lag_3",
    "cnt_lag_4",
    "cnt_lag_5",
    "cnt_lag_6",
]
CATEGORICAL_FEATURES = ["season", "mnth", "holiday", "weekday", "workingday", "weathersit"]

TARGET = "cnt"

RANDOM_STATE = 42

MLFLOW_TRACKING_URL = "http://localhost:4000"
MLFLOW_EXPERIMENT = "Bike sharing demand"

XGB_N_ESTIMATORS = [100, 200, 300]
XBG_LEARNING_RATE = [0.01, 0.1, 0.2]
XBG_MAX_DEPTH = [3, 5, 7]
XGB_SUBSAMPLE = [0.8, 1.0]
XGB_COLSAMPLE_BYTREE = [0.8, 1.0]
