import pandas as pd
from pathlib import Path


def prepare_features(df):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    df["lag_1"] = df["patient_arrivals"].shift(1)
    df["lag_7"] = df["patient_arrivals"].shift(7)
    df["rolling_7"] = df["patient_arrivals"].rolling(7).mean()
    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month

    return df.dropna()


def main(test_fraction=0.1):
    """Trains XGBoost on the earlier portion of the timeline and
    evaluates on a held-out later portion - fitting and predicting on
    the same rows (the original version of this script) isn't a real
    test of forecasting ability, just how well the model memorized
    the data it already saw."""
    from xgboost import XGBRegressor

    base_dir = Path(__file__).resolve().parent.parent
    df = pd.read_csv(base_dir / "data" / "features" / "forecast_dataset.csv")

    df = prepare_features(df)

    split_index = int(len(df) * (1 - test_fraction))
    train, test = df.iloc[:split_index], df.iloc[split_index:]

    features = ["lag_1", "lag_7", "rolling_7", "day_of_week", "month"]

    model = XGBRegressor()
    model.fit(train[features], train["patient_arrivals"])

    predictions = model.predict(test[features])

    return pd.DataFrame({
        "date": test["date"].values,
        "actual": test["patient_arrivals"].values,
        "predicted": predictions,
    })


if __name__ == "__main__":
    result = main()
    print(result.tail())
