import pandas as pd
from pathlib import Path


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
