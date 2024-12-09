import pandas as pd
from dagster import AutomationCondition, asset

from bike_share.config import CATEGORICAL_FEATURES, NUMERIC_FEATURES, TARGET


# TODO: Define the bike_rental_features asset here. Use the daily_bike_rental_demand as input to this asset.
