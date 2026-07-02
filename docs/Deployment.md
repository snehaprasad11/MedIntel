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

## Demo Assets

Demo media lives in:

```text
docs/demo/
docs/images/
```

`docs/demo/` contains captured Streamlit screenshots and an animated walkthrough GIF. `docs/images/` contains manually created Power BI dashboard screenshots.
