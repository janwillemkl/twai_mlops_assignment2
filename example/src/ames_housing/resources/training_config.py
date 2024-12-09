"""Model training configuration."""

from dagster import ConfigurableResource


class ModelTrainingConfig(ConfigurableResource):
    """Model hyperparameters."""

    learning_rate: float
    n_estimators: int
    random_state: int
