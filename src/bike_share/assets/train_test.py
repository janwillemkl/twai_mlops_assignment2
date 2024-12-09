import pandas as pd
from dagster import AssetOut, AutomationCondition, multi_asset
from sklearn.model_selection import train_test_split

from bike_share.config import RANDOM_STATE


# TODO: Define the train_test_data asset here. Instead of using @asset, use @multi_asset.
