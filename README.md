# Bike Share Demand Prediction

Bike-sharing systems have become a popular means of urban transportation, providing an eco-friendly, flexible, and cost-effective way to commute. These systems are widely adopted in cities worldwide, offering users the ability to rent bikes for short periods. Efficient management of these systems requires accurate demand forecasting to ensure optimal distribution of bikes across stations, reduce operational costs, and improve user satisfaction.

## The Problem

In this project, we focus on analyzing historical data from a bike-sharing system to predict **the number of bikes used for the next day**. Accurate demand prediction helps operators plan resource allocation, anticipate peak usage periods, and maintain a balanced supply across the network.

The data used for this analysis is from the UCI Bike Sharing Dataset, which includes daily bike rental counts along with various features influencing demand, such as weather conditions, seasons, holidays, and working days.

## Objective

The goal is to create an MLOps pipeline that trains a predictive model that can estimate the total number of bike rentals (`cnt`) based on historical data.

## Dataset Description

The dataset contains detailed records of bike rentals in a shared bike system, with the following key features:

**Seasonal and Temporal Factors:**

* `season`: Categorical variable representing the season (e.g., spring, summer).
* `yr`: Year of the observation.
* `mnth`: Month of the observation.
* `weekday`: Day of the week.
* `holiday`: Indicator for public holidays.
* `workingday`: Indicator for working days.

**Weather Conditions:**

* `temp`: Normalized temperature in Celsius.
* `hum`: Normalized humidity.
* `windspeed`: Normalized wind speed.
* `weathersit`: Categorical variable describing general weather conditions (e.g., clear, cloudy, rainy).

**Target Variable:**

* `cnt`: Total count of bikes rented (including registered and casual users).


## Notebook

In the `notebook` folder, you will find a Jupyter notebook designed to train and evaluate two machine learning models for predicting the number of bikes rented in a bike-sharing system. The notebook systematically implements a series of steps to preprocess data, engineer features, train models, and log results using MLflow.

The notebook performs the following tasks:

**Configuration Setup:**

* Sets the required configurations for the notebook environment.
* Configures MLflow with *autologging* enabled to seamlessly track experiments and log results.

**Data Reading:**

* Loads the dataset from the data directory, which contains the historical bike-sharing data with features such as weather, temporal information, and usage counts.

**Feature Engineering:**

* Adds the number of bikes used in the past 6 days as additional features to capture temporal patterns and improve the model’s predictive power.

**Dataset Splitting:**

* Splits the dataset into training and testing subsets to enable model training and evaluation on unseen data.

**Model Training:**

* Trains two machine learning models:
  * **Linear Regression Model**: A baseline model for comparison.
  * **XGBoost Model**: A gradient boosting model, with its hyperparameters optimized using `GridSearchCV`.

**Model Evaluation**:

* Evaluates both models using appropriate regression metrics to assess their performance.
* Logs evaluation results, model artifacts, and parameters to MLflow for easy tracking and reproducibility.


## Orchestration

In the `src/bike_share` directory, you will find a skeleton project for creating a *Dagster* pipeline to automate the training and evaluation of machine learning models for predicting bike-sharing demand. This pipeline is designed to mirror the functionality of the Jupyter notebook while adding automation and orchestration features.

To complete this project, implement the following components:

1. **Assets:**
    * Define the necessary Dagster assets for:
        * **Reading the dataset** from the specified directory.
        * **Feature engineering**, including adding the number of bikes used in the past 6 days as features and filtering unused columns.
        * **Splitting the dataset** into training and testing subsets.
        * **Training the models** (Linear Regression and XGBoost) and optimizing the hyperparameters for XGBoost using GridSearch.
2. **MLflow Session Resource**:
    * Use the MLflow session resource and add it to the model assets, allowing you to log experiment results, including metrics, hyperparameters, and model artifacts, directly from the pipeline. Add relevant data (asset name, dagster run id) to the run automatically.
3. **Sensor for Dataset Changes**:
    * Add a Dagster sensor that automatically detects changes to the dataset in the data directory. The sensor should trigger the pipeline whenever new data is added or existing data is modified.
4. **Automation for Model Training**:
    * Set up automation to train the models whenever the dataset changes, ensuring the pipeline is executed end-to-end whenever new data is detected by the sensor.


### Task 1: Define the assets

In the `src/bike_share/assets` folder, you will find the skeleton structure for defining the assets of the Dagster pipeline.


#### Asset 1: Daily bike rental demand (a.k.a. the raw data set)

One key component is the implementation of the `daily_bike_rental_demand` asset, which represents the loading of the bike-sharing dataset.

1. **Create the asset**:
    * Write the function `daily_bike_rental_demand` and annotate the function with the `@asset()` decorator.
2. **Load the Dataset**:

    * Use the `DatasetLoader` resource provided in `src/bike_share/resources/dataset_loader.py`.
    * Utilize the `load()` method of the `DatasetLoader` resource to load the CSV files in the data directory into a pandas `DataFrame`.
    * Ensure the dataset is returned as a pandas `DataFrame`, ready for downstream processing.
3. **Add the Asset to the Definitions**:
    * Add the asset to the definitions in `src/bike_share/__init__.py`.
4. **Locate the asset in the dagster user interface**:
    * Start the dagster development server using `dagster dev -m bike_share` and go to `http://localhost:3000` in the browser.
    * From the lineage view (locate this view by clicking on the octopus icon) you can materialize the asset by clicking "Materialize all".

#### Asset 2: Features

The next step in the pipeline is to implement the feature engineering asset, which is responsible for preparing the dataset for model training by adding engineered features and filtering for the selected ones. 

1. **Create the Asset**:
    * Write the function `bike_rental_features` and annotate the function with the `@asset()` decorator.
2. **Define Asset Dependencies**:
    * The input to this asset is the `daily_bike_rental_demand` asset, which provides the loaded dataset as a pandas `DataFrame`.
2. **Add Lagged Features**:
    * Calculate the number of bikes used in the past 6 days for each observation and include these as new features (`cnt_lag_1`, ..., `cnt_lag_6`).
3. **Filter Selected Features**:
    * Retain only the relevant features required for training the model, ensuring unnecessary columns are excluded. The selected features are defined as `NUMERIC_FEATURES`, `CATEGORICAL_FEATURES`, and `TARGET` for the target variable.
4. **Add the Asset to the Definitions**:
    * Add the asset to the definitions in `src/bike_share/__init__.py`.


#### Asset 3: Train-test Split:

The third step in the pipeline is to implement the train-test split asset, which splits the processed dataset into training and testing subsets. This asset is unique because it produces two assets (training and testing datasets) within a single Python function.

1. **Create the Asset**:
    * Write the function `train_test_data` and annotate the function with the `@multi_asset()` decorator.
    * Define the asset names within the decorator to explicitly specify the output assets.
2. **Define Asset Dependencies**:
    * The input to this asset is the `bike_rental_features` asset, which provides the feature and target as a pandas `DataFrame`.
3. **Split the Dataset**:
    * Split the dataset into training and testing subset. Return both subsets.
4. **Add the Asset to the Definitions**:
    * Add the asset to the definitions in `src/bike_share/__init__.py`.


#### Asset 4: Model training

The final step in this phase of the pipeline is the model training step, where two machine learning models are trained: a Linear Regression model and an XGBoost model. This step leverages a helper function for efficient model pipeline creation. Focus only on training the models in this step. Model performance evaluation will be handled in the subsequent task.

> Note: There seems to be a problem when using grid search using multiple concurrent processes in dagster. When implementing the model training assets, do not use `n_jobs=-1`.

1. **Create the Assets**:
    * Write the function `linear_regression` and annotate the function with the `@asset()` decorator.
    * Write the function `xgboost_regressor` and annotate the function with the `@asset()` decorator.
2. **Use the `create_pipeline` Helper Function**:
    * Pass the estimators for both models (Linear Regression and XGBoost) into the `create_pipeline` function to simplify the training pipeline creation.
3. **BONUS: Configurable Grid Search for XGBoost**:
    * Make the hyperparameters for the Grid Search on the XGBoost model configurable by creating a resource named `XGBRegressorGridSearchConfig`.
    * Define the hyperparameters grid as attributes of the `XGBRegressorGridSearchConfig` class.
    * Follow the structure and style of other resources in the resources directory.
    * Add your resource to the definitions in `src/bike_share/__init__.py`.
4. **Add the Asset to the Definitions**:
    * Add the asset to the definitions in `src/bike_share/__init__.py`.


### Task 2: Experiment tracking

The current model training assets train the prediction models but do not evaluate their performance or upload the assets to MLflow for tracking. In this task, you will integrate experiment tracking into the model training process using the `MlflowSession` resource.


1. **Use the MlflowSession Resource**:
    * The `MlflowSession` resource is defined in `src/bike_share/resources/mlflow_session.py`.
    * Inspect the code to understand how it tags the MLflow run with the asset key and Dagster run ID.
    * Note how the run name is composed of the `run_id` and `asset key` for easier identification in MLflow.
2. **Modify the Model Training Functions**:
    * Change the function headers to include the `AssetExecutionContext` and `MlflowSession` resources as input parameters

            @asset()
            def linear_regression(context: AssetExecutionContext, mlflow_session: MlflowSession, ...)
                ...

    * Start an MLflow run using:

            with mlflow_session.start_run(context):
                ...
            
    * Within the MLflow run, evaluate the model’s performance using the `evaluate` function.
3. **Run the pipeline and inspect results in Mlflow**:
    * Ensure both the Linear Regression and XGBoost models are logged to MLflow, along with their evaluation results.


### Task 3: Sensor for Dataset Changes

Until now, you’ve manually triggered the training pipeline by clicking the "Materialize All" button in the Dagster interface. In this task, you will integrate a sensor to automatically trigger the pipeline when there are changes to the data in the `data` directory.

1. **Define the Sensor**:
    * The sensor is already defined in `src/bike_share/sensors/data_directory_sensor.py`. Uncomment the code.
    * A sensor is a Python function annotated with the `@sensor` decorator and monitors for changes in external resources, such as files in a directory.
2. **Sensor Targets:**:
    * The `targets` of the sensor specify the assets to materialize when the sensor detects a change in the data directory.
    * In this case, the target is the `daily_bike_rental_demand` asset, representing the raw dataset.
3. **Run Request with Unique Run Key**:
    * The sensor uses a hash of the dataset as the `run_key` in the `RunRequest`.
    * Dagster ensures that the `daily_bike_rental_demand` asset is materialized only when a unique `run_key` is encountered.
4. **Add Sensor to Definitions**:
    * Add the sensor to the definitions in `src/bike_share/__init__.py`. (as `sensors=[...]`)
5. **Activate the Sensor**:
    * Navigate to the "Automation" page in the Dagster UI.
    * Enable the data_directory_changes sensor.
6. **Simulate a Data Change**:
    * Start with only the `day_2011.csv` file in the `data` directory.
    * Add a new file, `day_2012.csv`, to the data directory to simulate a change.
    * Observe the pipeline automatically starting in the Dagster UI. (Note: Starting the run may be delayed by up to 30 seconds.)


### Task 4: Automation

The sensor from Task 3 currently materializes only the `daily_bike_rental_demand` asset when there is a change in the data directory. In this task, you will declare materialization rules for downstream assets, ensuring that all dependent assets are materialized automatically whenever `daily_bike_rental_demand` changes.

1. **Declare Automation Rules for Downstream Assets**:
    * For each downstream asset (starting with `bike_rental_features`), add the `automation_condition=AutomationCondition.eager()` parameter to the `@asset` decorator. This specifies that the asset should be materialized automatically when upstream assets change.
2. **Handle `train_test_data`**:
    * For multi-asset outputs (e.g., `train_test_data`), add the `automation_condition` in the `AssetOut` declaration for each downstream asset.
3. **Enable Automation in the Dagster UI**:
    * Navigate to the "Automation" page in the Dagster UI and enable the `default_automation_condition_sensor` to apply the defined automation rules.
4. **Simulate a Data Change**:
    * Make sure only the `day_2011.csv` file exists in the `data` directory.
    * Restart the Dagster development server.
    * Simulate a data change by adding `day_2012.csv` to the `data` directory.
5. **Observe Materialization**:
    * Watch as the pipeline automatically materializes the `daily_bike_rental_demand` asset and all downstream assets (`bike_rental_features`, etc.). Note that the process may take up to a minute to initiate.


## References

This project uses the UCI Bike Sharing dataset found here: https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset

* Fanaee-T, H., & Gama, J. (2014). Event labeling combining ensemble detectors and background knowledge. Progress in Artificial Intelligence, 2(2-3), 113-127. Springer Berlin Heidelberg.