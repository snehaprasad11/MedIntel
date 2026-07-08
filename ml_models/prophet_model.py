import pandas as pd
from pathlib import Path


def backtest(test_fraction=0.1):
    """Fits Prophet on the earlier portion of the timeline only, then
    predicts for the held-out later portion's dates (which have known
    actual values) - for a fair comparison against the other models.
    This is separate from main(), which forecasts genuine future dates
    with no ground truth to compare against."""
    from prophet import Prophet

    base_dir = Path(__file__).resolve().parent.parent
    df = pd.read_csv(base_dir / "data" / "features" / "forecast_dataset.csv")

    split_index = int(len(df) * (1 - test_fraction))
    train, test = df.iloc[:split_index], df.iloc[split_index:]

    train_df = train[["date", "patient_arrivals"]].rename(columns={"date": "ds", "patient_arrivals": "y"})

    model = Prophet()
    model.fit(train_df)

    future = test[["date"]].rename(columns={"date": "ds"})
    forecast = model.predict(future)

    return pd.DataFrame({
        "date": test["date"].values,
        "actual": test["patient_arrivals"].values,
        "predicted": forecast["yhat"].values,
    })


def main():
    from prophet import Prophet

    base_dir = Path(__file__).resolve().parent.parent
    input_path = base_dir / "data" / "features" / "forecast_dataset.csv"
    output_path = base_dir / "data" / "features" / "prophet_forecast.csv"

    df = pd.read_csv(input_path)

    prophet_df = df[["date", "patient_arrivals"]].copy()
    prophet_df.columns = ["ds", "y"]

    model = Prophet()
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    forecast.to_csv(output_path, index=False)

    print("Prophet model completed")
    print("Saved at:", output_path)


if __name__ == "__main__":
    main()
