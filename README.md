# 🎬 Movie Analytics Platform
A **production-ready Movie Analytics Platform** built using **Python, Pandas, FastAPI, and Vanilla JavaScript**.

This project demonstrates how to design and implement a **clean analytics system** — from raw data ingestion to aggregated insights exposed via REST APIs and consumed by a lightweight frontend.

The focus is on **data engineering, analytics correctness, and architectural clarity**, not UI complexity.

---
## ❓ Problem Statement
Movie datasets (such as Kaggle / TMDB datasets) are often large, noisy, and not directly usable for analytics or applications.

Common challenges include:
- Inconsistent data types (dates, numbers as strings)
- Missing or null values
- Multi-valued categorical fields (e.g., genres)
- Unfair ranking of movies with very few votes
- Tight coupling between data processing and APIs
### Objective
Build a system that:
- Cleans and normalizes raw movie data
- Computes meaningful analytics (not raw rows)
- Exposes insights via clean, documented REST APIs
- Keeps analytics logic independent from API and frontend layers
- Demonstrates production-ready engineering practices
---
## 🏗 Architecture
### High-Level Data Flow
```
Raw CSV (Kaggle Dataset)
        │
        ▼
Pandas Preprocessing (cleaning & normalization)
        │
        ▼
Analytics Layer (Pure Pandas aggregations)
        │
        ▼
FastAPI (Aggregated REST endpoints)
        │
        ▼
Vanilla HTML / JavaScript (Read-only frontend)
```
### Architectural Principles
- **Separation of concerns**
  - Data processing, analytics, API, and UI are independent
- **Deterministic pipelines**
  - Same input → same output
- **Analytics-first design**
  - APIs return insights, not raw data
- **Frontend as a consumer**
  - No business logic in the UI
---
## 📂 Project Structure
```
movie-analytics-platform/
│
├── data/
│   ├── raw_movies.csv
│   └── cleaned_movies.csv
│
├── processing/
│   ├── preprocess.py
│   └── analytics.py
│
├── api/
│   ├── main.py
│   ├── routes.py
│   └── schemas.py
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
├── README.md
└── requirements.txt
```
---
## 🧹 Pandas Workflow (Data Processing)
### Step 1: Raw Data Ingestion (`preprocess.py`)
The raw dataset contains:
- Dates as strings
- Numeric values with possible missing entries
- Genres as comma-separated strings
- Long text fields (overview)
### Step 2: Cleaning & Normalization
Key operations performed using Pandas:
- Convert `Release_Date` to `datetime`
- Drop rows with invalid or missing dates
- Coerce numeric fields safely:
  - `Popularity`
  - `Vote_Count`
  - `Vote_Average`
- Handle missing categorical values
- Normalize multi-genre movies:
  - Split genre strings
  - Explode into one-genre-per-row
- Ensure deterministic ordering
### Step 3: Persist Clean Dataset
The cleaned output is saved as: `data/cleaned_movies.csv`

This file becomes the **single source of truth** for analytics and APIs.
---
## 📊 Analytics Layer (`analytics.py`)
This layer contains **pure Pandas functions** with no FastAPI or frontend dependencies.
### Key Analytics Implemented
- Movies released per year
- Average rating per genre
- Top N movies by popularity
- Top N movies by weighted rating
- Language-wise movie distribution
### Weighted Rating Logic
To avoid unfair rankings (e.g., movies with very few votes):

**Weighted Rating = (v / (v + m)) * R + (m / (v + m)) * C**

Where:
- R = average rating of the movie
- v = number of votes for the movie
- C = mean rating across the dataset
- m = vote count threshold (70th percentile)

This is similar to **IMDb’s rating methodology**.
## 🚀 REST API (FastAPI)
### Base URL
http://127.0.0.1:8000
### API Endpoints
| Endpoint | Method | Description |
|--------|--------|------------|
| `/movies/most-popular` | GET | Top movies by popularity |
| `/movies/top-rated` | GET | Top movies by weighted rating |
| `/movies/by-genre` | GET | Average rating per genre |
| `/movies/yearly-trends` | GET | Movies released per year |
| `/movies/language-stats` | GET | Language-wise distribution |
### Query Parameters
- `limit` (Most Popular / Top Rated)
  - Minimum: 1
  - Maximum: 50
- Enforced at API level using FastAPI validation
### Interactive Documentation
FastAPI automatically generates API docs: http://127.0.0.1:8000/docs
---
## 🖥 Frontend
- Built using **Vanilla HTML, CSS, and JavaScript**
- No frameworks or libraries
- Uses `fetch` to call FastAPI endpoints
- Displays results in tabular format
- Includes:
  - User-defined limits
  - Serial numbering
  - Clear UX hierarchy

The frontend is **read-only** and purely presentational.

---
## ▶️ How to Run Locally
### 1️⃣ Create & Activate Virtual Environment
#### macOS / Linux
```
python3 -m venv .venv
source .venv/bin/activate
```
#### Windows (PowerShell)
```
python -m venv .venv
.venv\Scripts\Activate.ps1
```
### 2️⃣ Install Dependencies
```
pip install -r requirements.txt
```
### 3️⃣ Run Data Preprocessing
```
python processing/preprocess.py
```
### 4️⃣ Start the API Server
#### Development mode (auto-reload)
```
uvicorn api.main:app --reload
```
#### With detailed logs (recommended for debugging)
```
uvicorn api.main:app --reload --log-level debug
```
##### You can now access:
- API root: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs
- Live request / error logs directly in the terminal
### 5️⃣ Open the Frontend
```
frontend/index.html
```