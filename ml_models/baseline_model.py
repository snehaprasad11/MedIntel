import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error

# =============================
# SAFE PROJECT PATH
# =============================
BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "data" / "features" / "forecast_dataset.csv"

print("Loading file from:", file_path)

# =============================
# LOAD DATA
# =============================
df = pd.read_csv(file_path)

# =============================
# SORT DATA
# =============================
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# =============================
# TARGET
# =============================
y = df["patient_arrivals"]

# =============================
# BASELINE MODELS
# =============================
df["naive_pred"] = y.shift(1)
df["ma_7"] = y.rolling(7).mean()

df = df.dropna()

# =============================
# EVALUATION FUNCTION
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
# RESULTS
# =============================
evaluate(df["patient_arrivals"], df["naive_pred"], "Naive Model")
evaluate(df["patient_arrivals"], df["ma_7"], "Moving Average (7-day)")