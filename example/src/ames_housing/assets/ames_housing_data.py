"""Ames housing data set."""

import pandas as pd
from dagster import asset

from ames_housing.constants import DATA_SET_URL


@asset(io_manager_key="csv_io_manager")
def ames_housing_data() -> pd.DataFrame:
    """Raw Ames housing dataset."""
    return pd.read_csv(DATA_SET_URL)


if __name__ == "__main__":
    raw_data = ames_housing_data()
    print(raw_data.head())
