"""Ames housing features."""

import pandas as pd
from dagster import AutomationCondition, asset

from ames_housing.constants import FEATURES, TARGET


@asset(automation_condition=AutomationCondition.eager())
def ames_housing_features(ames_housing_data: pd.DataFrame) -> pd.DataFrame:
    """Select features and target column from the raw features."""
    columns = (
        FEATURES["nominal"] + FEATURES["ordinal"] + FEATURES["numerical"] + [TARGET]
    )

    return ames_housing_data[columns]


if __name__ == "__main__":
    raw_data = pd.read_csv("data/ames_housing.csv")
    features = ames_housing_features(raw_data)

    print(features.head())
