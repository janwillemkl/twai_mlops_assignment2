from typing import Any

import mlflow
import pandas as pd
from dagster import AssetExecutionContext, AutomationCondition, asset
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBRegressor

from bike_share.config import CATEGORICAL_FEATURES, NUMERIC_FEATURES, RANDOM_STATE, TARGET
from bike_share.resources.mlflow_session import MlflowSession
from bike_share.resources.xgboost_regressor_config import XGBRegressorGridSearchConfig


def create_pipeline(estimator: Any) -> Pipeline:
    numeric_transformer = Pipeline([("scaler", StandardScaler())])

    categorical_transformer = Pipeline([("encoder", OneHotEncoder())])

    preprocessor = ColumnTransformer(
        [
            ("numeric", numeric_transformer, NUMERIC_FEATURES),
            ("categorical", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )

    pipeline = Pipeline(
        [
            ("preprocessor", preprocessor),
            (
                "estimator",
                estimator,
            ),
        ]
    )

    return pipeline


@asset()
def linear_regression(train_data: pd.DataFrame, test_data: pd.DataFrame) -> None:
    """Trains a linear regression model."""

    # TODO: Finish the linear regression asset.


@asset(automation_condition=AutomationCondition.eager())
def xgboost_regressor(
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
) -> None:
    """Trains an XGBoost regressor model."""

    # TODO: Finish the XGBoost regressor asset.
