import pandas as pd
from pathlib import Path
from prophet import Prophet

# =============================
# LOAD DATA
# =============================
BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "data" / "features" / "forecast_dataset.csv"

df = pd.read_csv(file_path)

# =============================
# PREP DATA FOR PROPHET
# =============================
prophet_df = df[["date", "patient_arrivals"]].copy()
prophet_df.columns = ["ds", "y"]

# =============================
# MODEL
# =============================
model = Prophet()
model.fit(prophet_df)

# =============================
# FORECAST
# =============================
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# =============================
# SAVE OUTPUT
# =============================
output_path = BASE_DIR / "data" / "features" / "prophet_forecast.csv"
forecast.to_csv(output_path, index=False)

print("Prophet model completed")
print("Saved at:", output_path)