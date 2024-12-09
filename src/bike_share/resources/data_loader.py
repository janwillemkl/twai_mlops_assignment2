import glob
import hashlib
import os

import pandas as pd
from dagster import ConfigurableResource


class DataLoader(ConfigurableResource):
    data_directory: str

    def load(self) -> pd.DataFrame:
        """Loads CSV files from the specified directory and combines them into a single DataFrame."""
        # List all CSV files in the data directory
        csv_files = glob.glob(os.path.join(self.data_directory, "*.csv"))

        # Read each CSV file into a DataFrame
        dataframes = [pd.read_csv(f) for f in csv_files]

        # Combine DataFrames into one
        return pd.concat(dataframes, ignore_index=True)

    def hash(self) -> str:
        """Calculates a hash of the data in the data directory."""
        data = self.load()

        data_str = data.to_csv(index=False)

        sha1_hash = hashlib.new("sha1")
        sha1_hash.update(data_str.encode("utf-8"))

        return sha1_hash.hexdigest()
