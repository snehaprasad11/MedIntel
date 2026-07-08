import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error


def compute_metrics(actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mape = float(np.mean(np.abs((actual - predicted) / actual)) * 100)
    return {"mae": round(mae, 2), "rmse": round(rmse, 2), "mape": round(mape, 2)}


def main(test_fraction=0.1):
    """Compares naive, 7-day moving average, XGBoost, and Prophet on
    the same held-out portion of the timeline, and saves the result
    to data/features/model_comparison.csv. This is what previously
    existed as three separate, never-run, print-only scripts
    (baseline_model.py, evaluation.py, xgboost_model.py) that never
    actually compared against each other."""
    from ml_models import prophet_model, xgboost_model

    base_dir = Path(__file__).resolve().parent.parent
    df = pd.read_csv(base_dir / "data" / "features" / "forecast_dataset.csv")
    df = df.sort_values("date").reset_index(drop=True)

    split_index = int(len(df) * (1 - test_fraction))
    test = df.iloc[split_index:]

    results = []

    naive_pred = df["patient_arrivals"].shift(1).iloc[split_index:]
    results.append({"model": "Naive (yesterday's value)", **compute_metrics(test["patient_arrivals"].values, naive_pred.values)})

    ma_pred = df["patient_arrivals"].rolling(7).mean().iloc[split_index:]
    results.append({"model": "7-Day Moving Average", **compute_metrics(test["patient_arrivals"].values, ma_pred.values)})

    xgb_result = xgboost_model.main(test_fraction=test_fraction)
    results.append({"model": "XGBoost", **compute_metrics(xgb_result["actual"].values, xgb_result["predicted"].values)})

    try:
        prophet_result = prophet_model.backtest(test_fraction=test_fraction)
        results.append({"model": "Prophet", **compute_metrics(prophet_result["actual"].values, prophet_result["predicted"].values)})
    except Exception as e:
        print(f"WARNING: Prophet backtest failed ({e}), skipping from comparison.")

    results_df = pd.DataFrame(results).sort_values("mae").reset_index(drop=True)

    output_path = base_dir / "data" / "features" / "model_comparison.csv"
    results_df.to_csv(output_path, index=False)

    print(results_df)
    print("Saved at:", output_path)

    return results_df


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    main()
