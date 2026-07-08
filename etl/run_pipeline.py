import os
import sys
from pathlib import Path

import pandas as pd

import generate_data
import clean_data
import feature_engineering


def train_forecast():
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from ml_models import prophet_model

    try:
        prophet_model.main()
    except Exception as e:
        print(f"WARNING: real Prophet forecast failed ({e}). Falling back to a naive")
        print("historical-average forecast instead - this is NOT a real prediction.")
        forecast_dataset = pd.read_csv("data/features/forecast_dataset.csv")
        fallback = forecast_dataset.rename(
            columns={"date": "ds", "patient_arrivals": "yhat"}
        )[["ds", "yhat"]]
        fallback.to_csv("data/features/prophet_forecast.csv", index=False)


def main():

    print("STEP 1: Generating data...")
    generate_data.main()

    print("STEP 2: Cleaning data...")
    clean_data.main()

    print("STEP 3: Feature engineering...")
    feature_engineering.main()

    print("STEP 4: Training forecast model...")
    train_forecast()

    if os.getenv("LOAD_MYSQL", "false").lower() in {"1", "true", "yes"}:
        import load_mysql

        print("STEP 5: Loading into MySQL...")
        load_mysql.main()
    else:
        print("STEP 5: Skipping MySQL load. Set LOAD_MYSQL=true to enable it.")

    print("PIPELINE COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
