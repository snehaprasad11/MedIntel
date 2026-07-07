# Deployment Guide

MedIntel has two deployment surfaces:

- **Streamlit dashboard**: the full Python dashboard in `dashboard/app.py`.
- **Netlify static preview**: the fast portfolio preview in `index.html`.

Netlify cannot run the Streamlit Python server directly. Use Netlify for the static preview and a Python-friendly host for the full dashboard.

## Local Streamlit Dashboard

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate local data:

```bash
python etl/run_pipeline.py
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

Open:

```text
http://localhost:8501
```

## MySQL-Backed Run

Run the canonical schema:

```text
sql/schema/create_tables.sql
```

Configure environment values from `.env.example`, then run:

```bash
LOAD_MYSQL=true python etl/run_pipeline.py
```

PowerShell:

```powershell
$env:LOAD_MYSQL="true"
python etl/run_pipeline.py
```

The schema resets the `medintel` database. Use it for fresh setup or rebuilds.

## Netlify Static Preview

The static preview uses:

- `index.html`
- `assets/site.css`
- `assets/site.js`
- `analytics/output/*.csv`
- `docs/images/*.png`

Netlify settings:

```text
Build command: empty
Publish directory: .
```

The static preview is intentionally lightweight. It loads precomputed CSV KPI outputs and dashboard images, so it is fast and does not require Python, Streamlit, MySQL, or model execution.

## Recommended Public Deployment

For a complete portfolio setup:

1. Deploy the static preview to Netlify.
2. Deploy the Streamlit app separately on Streamlit Community Cloud, Render, Railway, or another Python host.
3. Link the hosted Streamlit dashboard from the Netlify page or README.

### Why there's a `dashboard/requirements.txt`

`dashboard/app.py` and everything under `dashboard/pages/` only import `pandas` and `streamlit` at runtime — they read pre-computed CSVs from `data/`, they never call Prophet, XGBoost, or MySQL live (those are only used by the offline `etl/` and `analytics/` scripts). `prophet` in particular is slow and prone to build failures on constrained cloud build environments, since it compiles Stan under the hood.

Streamlit Community Cloud looks for a `requirements.txt` in the same folder as the app's main file first, before falling back to the repo root — there is no manual "pick a dependencies file" option in its deploy UI. So `dashboard/requirements.txt` (just `pandas` + `streamlit`) is what actually gets installed when deploying with **Main file path: `dashboard/app.py`**, automatically, with nothing to configure. The root `requirements.txt` (with the full pipeline dependencies) is only used for local development when running the whole ETL/ML pipeline.

## Demo Assets

Demo media lives in:

```text
docs/demo/
docs/images/
```

`docs/demo/` contains captured Streamlit screenshots and an animated walkthrough GIF. `docs/images/` contains manually created Power BI dashboard screenshots.
