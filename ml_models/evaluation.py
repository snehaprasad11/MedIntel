import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from pathlib import Path

# =============================
# LOAD DATA
# =============================
BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "data" / "features" / "forecast_dataset.csv"

df = pd.read_csv(file_path)

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# =============================
# BASELINE (NAIVE)
# =============================
df["naive"] = df["patient_arrivals"].shift(1)

df = df.dropna()

# =============================
# METRICS FUNCTION
# =============================
def evaluate(true, pred, name):
    mae = mean_absolute_error(true, pred)
    rmse = np.sqrt(mean_squared_error(true, pred))
    mape = np.mean(np.abs((true - pred) / true)) * 100

    print("\n", name)
    print("MAE:", mae)
    print("RMSE:", rmse)
    print("MAPE:", mape)

# =============================
# EVALUATE BASELINE
# =============================
evaluate(df["patient_arrivals"], df["naive"], "Naive Model")