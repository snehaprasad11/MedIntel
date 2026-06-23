# MedIntel – Healthcare Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue)
![Machine Learning](https://img.shields.io/badge/ML-Forecasting-orange)
![Status](https://img.shields.io/badge/Status-Completed-success)
## End-to-End AI + Data Engineering + Analytics System for Hospital Operations

MedIntel is a full-stack healthcare intelligence platform that transforms raw hospital operational data into structured insights, predictive analytics, and AI-assisted decision support.

It integrates a complete analytics ecosystem:
- Data Engineering (ETL pipelines)
- SQL-based Analytics (KPI generation layer)
- Machine Learning (forecasting + anomaly detection)
- AI Layer (LLM-based insights + recommendations)
- Business Intelligence (Streamlit dashboards + Power BI reports)
- Modular system architecture designed for scalability

---

# Problem Statement

Modern hospital systems face operational inefficiencies such as:

- Lack of visibility into patient flow and waiting time drivers
- Uneven doctor workload distribution across departments
- Inability to forecast patient demand accurately
- Fragmented reporting across departments and systems
- Heavy reliance on static dashboards or manual Excel-based reporting

These limitations prevent data-driven operational decision-making and proactive resource planning.

---

# Solution: MedIntel Intelligence System

MedIntel addresses these challenges by building an end-to-end data-to-insights pipeline:

Raw Hospital Data → ETL Pipeline → MySQL Database → SQL Analytics Layer → ML Forecasting Engine → AI Insight Generator → Streamlit Dashboard + Power BI Reports

---

# System Architecture

## 1. Data Layer

The system uses structured synthetic hospital datasets representing real-world hospital operations.

Entities include:
- Patients
- Doctors
- Departments
- Appointments
- Beds
- Equipment
- Staff

This layer simulates realistic hospital operational data.

---

## 2. ETL Layer (`/etl`)

The ETL layer is responsible for data preparation and pipeline orchestration:

- Data generation (`generate_data.py`)
- Data cleaning (`clean_data.py`)
- Feature engineering (`feature_engineering.py`)
- MySQL ingestion (`load_mysql.py`)
- Pipeline execution (`run_pipeline.py`)

This transforms raw datasets into analytics-ready structured data.

---

## 3. Database Layer (MySQL)

A normalized relational schema acts as the core data warehouse layer.

Key analytical views:
- vw_daily_operations
- vw_department_summary
- vw_doctor_performance

This layer serves as the single source of truth for analytics and ML workflows.

---

## 4. SQL Analytics Layer (`/sql`)

This layer converts raw structured data into business KPIs.

Key analytical areas:
- Patient inflow trends
- Doctor utilization and workload analysis
- Department-level performance metrics
- Hourly and daily traffic patterns
- Weekend vs weekday operational differences

This acts as the business intelligence transformation layer.

---

## 5. Machine Learning Layer (`/ml_models`)

The ML layer provides predictive intelligence on hospital operations.

### Models implemented:
- Prophet (time-series forecasting)
- XGBoost (feature-based prediction)
- Anomaly detection model
- Evaluation framework for model performance

### Outputs:
- Patient demand forecasting
- Department-level load prediction
- Resource utilization forecasting

---

## 6. AI Insights Engine (`/ai_insights`)

This layer converts structured analytics outputs into natural language insights.

Capabilities:
- KPI summarization using LLM-based pipelines
- Automated operational insight generation
- Recommendation system for hospital efficiency
- Prompt-engineered insight generation from structured SQL outputs

Example output:
“Emergency department load is significantly above baseline during peak hours, indicating a need for dynamic staff reallocation.”

---

## 7. Dashboard Layer (`/dashboard`)

A multi-page Streamlit application for interactive analytics:

- Executive Overview Dashboard
- Analytics & KPI Exploration
- Forecasting Dashboard
- Doctor Performance Analysis
- Resource Utilization Monitoring
- AI Insights Panel

This layer serves as the primary user-facing analytics interface.

---

# Power BI Integration

Power BI is used as an executive reporting layer to complement the Streamlit dashboard.

## Included Dashboards:
- Executive Hospital Overview
- Department Performance Analysis
- Doctor Workload Distribution
- Operational Heatmaps and KPI Trends

## Location:
`/docs/images/`

These dashboards simulate executive-level reporting used in enterprise BI systems.

---

# API Integration (Future Ready Design)

The system architecture is designed to support future API-based expansion.

Planned enhancements:
- FastAPI layer for data access and model serving
- Real-time hospital data ingestion pipelines
- Integration with external EHR systems
- Live dashboard updates
- Cloud deployment (AWS/GCP)

---

# Key Features

## Intelligence Layer
- AI-generated hospital operational insights
- Automated KPI narrative summaries
- Predictive workload forecasting

## Analytics Layer
- Doctor performance ranking system
- Department-level load analysis
- Wait time and bottleneck detection
- Operational efficiency tracking

## Engineering Layer
- Modular ETL pipeline architecture
- SQL-based analytics warehouse design
- Feature-engineered datasets for ML
- Cached dashboard service layer

---

# Tech Stack

## Programming Language
- Python 3.10+

## Data Engineering
- Pandas
- NumPy
- MySQL

## Machine Learning
- Prophet
- XGBoost
- Scikit-learn

## AI Layer
- OpenAI API (LLM-based insights)
- Prompt engineering framework

## Visualization
- Streamlit
- Power BI

## Database
- MySQL (relational schema + analytical views)

## Tools & Version Control
- Git & GitHub
- Modular Python architecture

---

# Business Impact (Simulated)

MedIntel demonstrates how data-driven hospital systems can improve operational efficiency by enabling:

- Reduced patient waiting time through demand visibility
- Improved doctor workload balancing
- Predictive staffing and resource allocation
- Identification of operational bottlenecks
- Executive-level visibility into hospital KPIs

---

# What I Learned

## Data Engineering
- Designing ETL pipelines from scratch
- Building structured analytical data models
- Feature engineering for operational datasets

## Machine Learning
- Time-series forecasting with real-world constraints
- Model evaluation and comparison techniques
- Feature-driven prediction systems

## AI Systems
- LLM-based insight generation pipelines
- Prompt engineering for structured data summarization
- Combining ML outputs with natural language explanations

## Full-Stack Analytics Engineering
- Building multi-page Streamlit applications
- Designing SQL-based analytics layers
- Integrating Power BI with Python pipelines

## System Design Thinking
- Modular architecture design
- Separation of concerns across layers
- Scalable analytics system design principles

---

# Industry Use Cases

MedIntel can be adapted for:

- Hospital operations optimization systems
- Patient flow prediction platforms
- Workforce and resource management tools
- Enterprise BI + AI decision platforms
- Healthcare analytics dashboards

---

# Future Enhancements

- Real-time streaming data pipeline (Kafka / Spark)
- FastAPI backend for model serving and APIs
- Cloud deployment (AWS / GCP)
- Role-based authentication system
- Advanced anomaly detection models
- Integration with real hospital EHR systems

---

# Final Outcome

MedIntel is a complete end-to-end AI-powered hospital intelligence system that demonstrates:

- Data Engineering (ETL + SQL modeling)
- Machine Learning (forecasting + anomaly detection)
- AI Systems (LLM-based insight generation)
- Business Intelligence (Streamlit + Power BI)
- Full-stack analytics engineering

---

# Recruiter Summary

This project demonstrates the ability to:

- Build production-style data pipelines
- Design scalable analytics architectures
- Apply machine learning to operational datasets
- Integrate AI with structured data systems
- Build interactive dashboards for decision-making
- Think in system design and end-to-end product terms