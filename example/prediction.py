import mlflow
import mlflow.pyfunc
import pandas as pd

mlflow.set_tracking_uri("http://localhost:4000")

MODEL_NAME = "ames_housing_model"
ALIAS = "staging"

model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}@{ALIAS}")


def predict(input: pd.DataFrame) -> float:
    prediction = model.predict(input)
    return prediction.tolist()[0]


if __name__ == "__main__":
    input_data = pd.DataFrame(
        [
            {
                "Unnamed: 0": 0,
                "ms_zoning": "RL",
                "lot_shape": "IR1",
                "land_contour": "Lvl",
                "land_slope": "Gtl",
                "overall_qual": 6,
                "overall_cond": 5,
                "lot_frontage": 141.0,
                "lot_area": 61770,
                "mas_vnr_area": 112.0,
            }
        ]
    )

    predicted_house_price = predict(input_data)
    print(f"Predicted house price = {predicted_house_price}")
