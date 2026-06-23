import pandas as pd
from pathlib import Path
from xgboost import XGBRegressor

# =============================
# LOAD DATA
# =============================
BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "data" / "features" / "forecast_dataset.csv"

df = pd.read_csv(file_path)

# =============================
# FEATURE ENGINEERING
# =============================
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

df["lag_1"] = df["patient_arrivals"].shift(1)
df["lag_7"] = df["patient_arrivals"].shift(7)
df["rolling_7"] = df["patient_arrivals"].rolling(7).mean()

df["day_of_week"] = df["date"].dt.dayofweek
df["month"] = df["date"].dt.month

df = df.dropna()

# =============================
# FEATURES + TARGET
# =============================
features = ["lag_1", "lag_7", "rolling_7", "day_of_week", "month"]

X = df[features]
y = df["patient_arrivals"]

# =============================
# MODEL
# =============================
model = XGBRegressor()
model.fit(X, y)

df["xgb_pred"] = model.predict(X)

print(df[["date", "patient_arrivals", "xgb_pred"]].tail())