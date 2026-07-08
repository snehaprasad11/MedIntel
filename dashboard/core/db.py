import os

import bcrypt
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text


def _config(key, default=None):
    """Streamlit Cloud provides credentials via st.secrets (TOML), set
    in its dashboard - it never reads .env files. Local development
    uses .env via python-dotenv into os.environ. Check secrets first,
    fall back to the environment, so the same code works in both."""
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.environ.get(key, default)


@st.cache_resource
def get_engine():
    db_host = _config("DB_HOST")
    db_port = _config("DB_PORT")
    db_user = _config("DB_USER")
    db_password = _config("DB_PASSWORD")
    db_name = _config("DB_NAME", "medintel")

    connect_args = {"ssl": {"ssl": {}}}

    server_engine = create_engine(
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/",
        connect_args=connect_args,
    )
    with server_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
        conn.commit()

    engine = create_engine(
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
        connect_args=connect_args,
    )
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS hospitals (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS department_snapshots (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hospital_id INT NOT NULL,
                department_name VARCHAR(255) NOT NULL,
                total_beds INT NOT NULL,
                occupied_beds INT NOT NULL,
                total_icu_beds INT NOT NULL,
                occupied_icu_beds INT NOT NULL,
                doctors_scheduled INT NOT NULL,
                doctors_present INT NOT NULL,
                nurses_scheduled INT NOT NULL,
                nurses_present INT NOT NULL,
                avg_wait_time_minutes FLOAT NOT NULL DEFAULT 0,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE CASCADE,
                INDEX idx_hospital_submitted (hospital_id, submitted_at)
            )
        """))
        conn.commit()

    return engine


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def create_hospital(engine, name, email, password):
    """Returns (success, message)."""
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    with engine.connect() as conn:
        existing = conn.execute(
            text("SELECT id FROM hospitals WHERE email = :email"),
            {"email": email},
        ).fetchone()
        if existing:
            return False, "An account with that email already exists."

        try:
            conn.execute(
                text("INSERT INTO hospitals (name, email, password_hash) VALUES (:name, :email, :password_hash)"),
                {"name": name, "email": email, "password_hash": password_hash},
            )
            conn.commit()
            return True, "Account created."
        except Exception as e:
            if "Duplicate entry" in str(e):
                return False, "That hospital name or email is already taken."
            return False, f"Could not create account: {e}"


def verify_login(engine, email, password):
    """Returns the hospital row (id, name, email) on success, or None."""
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT id, name, email, password_hash FROM hospitals WHERE email = :email"),
            {"email": email},
        ).fetchone()

    if row is None:
        return None

    if bcrypt.checkpw(password.encode("utf-8"), row.password_hash.encode("utf-8")):
        return {"id": row.id, "name": row.name, "email": row.email}

    return None


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def submit_snapshot(engine, hospital_id, department_name, total_beds, occupied_beds,
                     total_icu_beds, occupied_icu_beds, doctors_scheduled, doctors_present,
                     nurses_scheduled, nurses_present, avg_wait_time_minutes=0):
    """Validates and inserts one department snapshot. Returns (success, message)."""

    errors = []
    if occupied_beds > total_beds:
        errors.append("Occupied beds can't exceed total beds.")
    if occupied_icu_beds > total_icu_beds:
        errors.append("Occupied ICU beds can't exceed total ICU beds.")
    if doctors_present > doctors_scheduled:
        errors.append("Doctors present can't exceed doctors scheduled.")
    if nurses_present > nurses_scheduled:
        errors.append("Nurses present can't exceed nurses scheduled.")
    if min(total_beds, occupied_beds, total_icu_beds, occupied_icu_beds,
           doctors_scheduled, doctors_present, nurses_scheduled, nurses_present, avg_wait_time_minutes) < 0:
        errors.append("Values can't be negative.")
    if not department_name.strip():
        errors.append("Department name can't be empty.")

    if errors:
        return False, " ".join(errors)

    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO department_snapshots (
                    hospital_id, department_name, total_beds, occupied_beds,
                    total_icu_beds, occupied_icu_beds, doctors_scheduled, doctors_present,
                    nurses_scheduled, nurses_present, avg_wait_time_minutes
                ) VALUES (
                    :hospital_id, :department_name, :total_beds, :occupied_beds,
                    :total_icu_beds, :occupied_icu_beds, :doctors_scheduled, :doctors_present,
                    :nurses_scheduled, :nurses_present, :avg_wait_time_minutes
                )
            """),
            {
                "hospital_id": hospital_id, "department_name": department_name.strip(),
                "total_beds": total_beds, "occupied_beds": occupied_beds,
                "total_icu_beds": total_icu_beds, "occupied_icu_beds": occupied_icu_beds,
                "doctors_scheduled": doctors_scheduled, "doctors_present": doctors_present,
                "nurses_scheduled": nurses_scheduled, "nurses_present": nurses_present,
                "avg_wait_time_minutes": avg_wait_time_minutes,
            },
        )
        conn.commit()

    return True, "Update submitted."


def get_latest_snapshots(engine, hospital_id):
    """Most recent snapshot per department for this hospital."""
    query = text("""
        SELECT s.*
        FROM department_snapshots s
        INNER JOIN (
            SELECT department_name, MAX(submitted_at) AS max_submitted
            FROM department_snapshots
            WHERE hospital_id = :hospital_id
            GROUP BY department_name
        ) latest
        ON s.department_name = latest.department_name AND s.submitted_at = latest.max_submitted
        WHERE s.hospital_id = :hospital_id
    """)
    with engine.connect() as conn:
        return pd.read_sql(query, conn, params={"hospital_id": hospital_id})


def get_snapshot_history(engine, hospital_id):
    """Full submission history for this hospital, oldest first - used for forecasting."""
    query = text("""
        SELECT * FROM department_snapshots
        WHERE hospital_id = :hospital_id
        ORDER BY submitted_at ASC
    """)
    with engine.connect() as conn:
        return pd.read_sql(query, conn, params={"hospital_id": hospital_id})
