from dagster import RunRequest, sensor

# from bike_share.assets.daily_bike_rental_demand import daily_bike_rental_demand
# from bike_share.resources.data_loader import DataLoader


# @sensor(target=[daily_bike_rental_demand])
# def data_directory_changes(data_loader: DataLoader):
#     yield RunRequest(run_key=data_loader.hash())
