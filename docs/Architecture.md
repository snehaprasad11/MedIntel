# MedIntel – System Architecture

## Overview
MedIntel is an end-to-end healthcare intelligence platform that transforms raw hospital operational data into actionable insights using ETL pipelines, SQL analytics, ML forecasting, and AI-driven decision systems.

---

## Architecture Layers

### 1. Data Layer
- Synthetic + Clean datasets stored in `/data`
- Entities:
  - patients
  - doctors
  - departments
  - appointments
  - beds
  - equipment

---

### 2. ETL Layer (`/etl`)
Responsible for data generation, cleaning, feature engineering, and database loading.

Modules:
- generate_data.py → synthetic data creation
- clean_data.py → preprocessing
- feature_engineering.py → derived KPIs
- load_mysql.py → DB ingestion
- run_pipeline.py → orchestration

---

### 3. Database Layer (MySQL)
- Normalized schema
- Analytical views:
  - vw_daily_operations
  - vw_department_summary
  - vw_doctor_performance

---

### 4. Analytics Layer (`/sql`, `/analytics`)
- KPI queries
- Operational insights
- Aggregations for BI tools

---

### 5. ML Layer (`/ml_models`)
- Forecasting: Prophet
- Gradient boosting: XGBoost
- Anomaly detection
- Evaluation pipeline

---

### 6. AI Insights Layer (`/ai_insights`)
- LLM-based summarization
- KPI interpretation engine
- Recommendation engine
- Prompt engineering system

---

### 7. Dashboard Layer (`/dashboard`)
Streamlit-based multi-page application:
- Executive view
- Analytics view
- Forecasting
- Doctor performance
- AI insights

---

## Data Flow

Raw Data → ETL → MySQL → SQL Views → ML Models → AI Engine → Dashboard