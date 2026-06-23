import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

# =============================
# LOAD DATA
# =============================
df = pd.read_csv("../data/features/forecast_dataset.csv")

# =============================
# SORT BY DATE
# =============================
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# =============================
# TARGET
# =============================
y = df["patient_arrivals"]

# =============================
# BASELINE 1: NAIVE (yesterday = today)
# =============================
df["naive_pred"] = y.shift(1)

# =============================
# BASELINE 2: MOVING AVERAGE (7 days)
# =============================
df["ma_7"] = y.rolling(7).mean()

# =============================
# CLEAN NA VALUES
# =============================
df = df.dropna()

# =============================
# EVALUATION FUNCTION
# =============================
def evaluate(true, pred, name):
    mae = mean_absolute_error(true, pred)
    rmse = np.sqrt(mean_squared_error(true, pred))
    mape = np.mean(np.abs((true - pred) / true)) * 100

    print(f"\n{name}")
    print("MAE:", mae)
    print("RMSE:", rmse)
    print("MAPE:", mape)

# =============================
# EVALUATE MODELS
# =============================
evaluate(df["patient_arrivals"], df["naive_pred"], "Naive Model")
evaluate(df["patient_arrivals"], df["ma_7"], "Moving Average (7-day)")