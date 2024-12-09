"""Train and test data sets."""

import pandas as pd
from dagster import AssetOut, AutomationCondition, multi_asset
from sklearn.model_selection import train_test_split

from ames_housing.constants import RANDOM_STATE


@multi_asset(
    outs={
        "train_data": AssetOut(
            io_manager_key="csv_io_manager",
            automation_condition=AutomationCondition.eager(),
        ),
        "test_data": AssetOut(
            io_manager_key="csv_io_manager",
            automation_condition=AutomationCondition.eager(),
        ),
    }
)
def train_test_data(
    ames_housing_features: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split the data set in a training and testing subset."""
    train_data, test_data = train_test_split(
        ames_housing_features, random_state=RANDOM_STATE
    )
    return train_data, test_data
