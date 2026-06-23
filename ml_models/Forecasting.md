# Hospital Demand Forecasting System

## Overview
This project builds a time-series forecasting system for hospital operations including:
- Patient arrivals prediction
- Bed demand forecasting
- ICU occupancy trends
- Department load estimation

---

## Data Pipeline
- Raw hospital operational data
- Feature engineering into time-series dataset
- Aggregation by date

---

## Models Used

### 1. Baseline Models
- Naive forecast (t-1)
- Moving average (7-day)

### 2. Prophet Model
- Captures seasonality and trends
- Suitable for hospital demand patterns

### 3. XGBoost Model
- Uses lag features
- Captures nonlinear relationships
- Includes rolling statistics and time features

---

## Evaluation Metrics
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error)

---

## Key Insight
XGBoost performs best due to ability to learn nonlinear patterns in hospital demand data.

---

## Future Improvements
- Deploy API using FastAPI
- Integrate with Power BI dashboard
- Real-time forecasting pipeline