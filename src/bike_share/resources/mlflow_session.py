import mlflow
from dagster import AssetExecutionContext, ConfigurableResource, InitResourceContext


class MlflowSession(ConfigurableResource):
    tracking_url: str
    experiment: str

    def setup_for_execution(self, context: InitResourceContext) -> None:
        mlflow.set_tracking_uri(self.tracking_url)
        mlflow.set_experiment(self.experiment)

        mlflow.autolog(log_datasets=False)

    def start_run(self, context: AssetExecutionContext) -> mlflow.ActiveRun:
        asset_key = context.asset_key.to_user_string()
        run_id = context.run.run_id[:8]

        run_name = f"{run_id}-{asset_key}"

        tags = {
            "dagster.asset": asset_key,
            "dagster.run_id": run_id,
        }

        return mlflow.start_run(run_name=run_name, tags=tags)
