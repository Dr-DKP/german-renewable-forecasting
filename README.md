# German Renewable Energy Forecasting Pipeline

**Solar & Wind Generation Prediction Using Real German Grid Data (SMARD)**

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Data Source](https://img.shields.io/badge/Data-SMARD%20Bundesnetzagentur-green)](https://www.smard.de/)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

> An end-to-end forecasting system for German renewable energy generation, from data ingestion through model comparison to uncertainty-calibrated predictions. Built with the same data sources that commercial energy forecasting companies use in production.

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Motivation & Background](#2-motivation--background)
3. [Data Sources](#3-data-sources)
4. [System Architecture](#4-system-architecture)
5. [Phased Roadmap](#5-phased-roadmap)
6. [Model Strategy: Prophet → XGBoost → LSTM](#6-model-strategy-prophet--xgboost--lstm)
7. [Uncertainty Quantification](#7-uncertainty-quantification)
8. [Infrastructure & MLOps](#8-infrastructure--mlops)
9. [Tech Stack & Rationale](#9-tech-stack--rationale)
10. [Key Design Decisions](#10-key-design-decisions)
11. [Project Structure](#11-project-structure)
12. [How to Run](#12-how-to-run)
13. [Results & Benchmarks](#13-results--benchmarks)
14. [Lessons Learned](#14-lessons-learned)
15. [License & Contact](#15-license--contact)

---

## 1. Problem Statement

Germany's Energiewende (energy transition) targets 80% renewable electricity by 2030. The challenge: solar and wind generation are **volatile and weather-dependent**. Unlike dispatchable power plants, you cannot simply "turn up" the sun.

**The operational problem for grid operators and energy traders:**

- A 10% forecasting error on solar generation at peak demand costs real money in balancing energy purchases on the spot market.
- Operators need not just a point estimate ("we expect 12 GW tomorrow at noon") but a **reliable uncertainty range** ("we expect 12 GW ± 2 GW, and here is our confidence").
- Most open-source forecasting projects stop at RMSE metrics. This project goes further: **what does the uncertainty actually mean for an operator's decision?**

This pipeline forecasts hourly solar and wind generation for Germany using publicly available SMARD data, compares three modeling approaches with increasing complexity, and outputs calibrated uncertainty estimates alongside point predictions.

---

## 2. Motivation & Background

### 2.1 Why This Domain

Renewable energy forecasting sits at the intersection of physics, data science, and operational decision-making. The data is real, the stakes are tangible, and the problems are genuinely hard: seasonal patterns, weather coupling, grid events, missing data, and the need for honest uncertainty estimates.

I chose this domain deliberately because it demands the kind of thinking I was trained in: understanding the physics driving the signal, designing systematic experiments, and treating uncertainty as a first-class output rather than an afterthought.

### 2.2 Physics Research → Applied Forecasting

My PhD and postdoc work in experimental physics maps directly to this problem:

| Research Skill | Direct Mapping in This Project |
|---|---|
| Time-resolved spectroscopy (femtosecond pump-probe) | Time-series feature engineering, lag variables, rolling statistics |
| Fourier analysis of optical signals | Seasonal decomposition of energy data (daily, weekly, annual cycles) |
| Uncertainty propagation in experimental measurements | Uncertainty quantification on model forecasts (prediction intervals) |
| Experimental design and hypothesis testing | Model comparison framework with statistical validation |
| Data pipeline automation (Python, LabVIEW) | Automated SMARD API ingestion and preprocessing |

The domain changes; the quantitative thinking does not. I am not learning data science from scratch. I am translating a decade of scientific training into an industrial forecasting context.

### 2.3 Industry Relevance

This pipeline mirrors the core workflow of commercial renewable energy forecasting: ingest official grid data, build models of increasing sophistication, produce calibrated probabilistic forecasts, and deliver results through an operational interface. The tools and data sources used here (SMARD, DWD, XGBoost, conformal prediction) are the same ones used in production energy forecasting systems across the DACH region.

---

## 3. Data Sources

### Primary: SMARD (Bundesnetzagentur)

**URL:** [https://www.smard.de/en](https://www.smard.de/en)

SMARD (Strommarktdaten) is Germany's official electricity market data platform, operated by the Federal Network Agency. It provides:

- Hourly generation by source (solar, wind onshore, wind offshore, hydro, biomass, nuclear, coal, gas)
- Electricity consumption (actual and forecasted)
- Import/export to neighboring countries
- Spot market prices (EPEX)

**Why SMARD specifically?**

1. **It's what industry uses.** The same data source that commercial forecasting providers work with.
2. **It has real-world messiness:** missing hours, outliers from grid events, DST transitions, public holiday effects. These are exactly the preprocessing challenges encountered in production.
3. **It's publicly documented and legally free.** Reproducible by anyone who reads this README.
4. **It has a REST API.** This forces a real data ingestion pipeline, not just a CSV download.

### Secondary: DWD (Deutscher Wetterdienst, Phase 2)

Solar and wind generation are physically driven by weather. A forecasting model that ignores weather is only extrapolating historical patterns; one that includes weather can respond to predicted conditions.

**DWD Open Data:** [https://opendata.dwd.de/](https://opendata.dwd.de/)

Features to extract:
- Solar irradiance (GHI, Global Horizontal Irradiance)
- Wind speed at 10m and 100m heights
- Cloud cover
- Temperature (affects solar panel efficiency, a detail most tutorials ignore)

> **Scope note:** Phase 1 builds a solid baseline using SMARD data alone. Weather feature integration is Phase 2. This is deliberate: establish what the historical pattern alone can predict before adding external covariates.

---

## 4. System Architecture

The pipeline is designed in four independent stages. Each stage has clear inputs, outputs, and can be tested and replaced without affecting the others.

```
┌─────────────────────────────────────────────────────────┐
│                   DATA INGESTION LAYER                  │
│                                                         │
│  SMARD API ──► Raw JSON ──► Validated Parquet Files     │
│  DWD API   ──► Raw CSV  ──►  (data/raw/)                │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│               FEATURE ENGINEERING LAYER                 │
│                                                         │
│  ► Temporal features (hour, day, week, month, season)   │
│  ► Lag features (t-1h, t-24h, t-168h)                   │
│  ► Rolling statistics (mean, std, 24h/7d windows)       │
│  ► Fourier terms (daily & annual seasonality)           │
│  ► Weather coupling (Phase 2)                           │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  MODELING LAYER                         │
│                                                         │
│  Model 1: Prophet  ──────────────────────────┐          │
│  Model 2: XGBoost  ──────────────────────────┤──► UQ    │
│  Model 3: LSTM     ──────────────────────────┘  layer   │
│                                                         │
│  Evaluation: RMSE, MAE, MAPE, Coverage, Sharpness       │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│               DEPLOYMENT & VISUALIZATION LAYER          │
│                                                         │
│  Streamlit Dashboard ──► Interactive forecast viewer    │
│  MLflow Tracking    ──► Experiment log & model registry │
│  FastAPI Endpoint   ──► /predict REST API (Phase 4)     │
└─────────────────────────────────────────────────────────┘
```

### Architectural principle: modularity over monolith

Each stage is a separate Python module. A broken API response in ingestion does not corrupt the modeling layer. Models can be swapped without touching the dashboard. This is a systems engineering principle, designed for maintainability and independent testing of each component.

---

## 5. Phased Roadmap

Building incrementally with working deliverables at each phase. Each phase has a clear exit criterion.

### Phase 0: Setup & Data Exploration (Week 1) - *Current*

**Goal:** Understand the data before touching a model.

- [ ] Set up project environment (conda/venv, `requirements.txt`)
- [ ] Implement SMARD API client (`src/data/smard_client.py`)
- [ ] Download historical solar + wind data (2018–2025)
- [ ] Exploratory Data Analysis notebook (`notebooks/01_eda.ipynb`)
  - Daily/weekly/seasonal patterns
  - Missing value analysis
  - Outlier identification (grid events, data gaps)
  - Autocorrelation structure (ACF/PACF plots)
- [ ] Document findings: what does the data tell us before modeling?

**Exit criterion:** EDA notebook complete, patterns understood, data quality issues documented.

---

### Phase 1: Baseline Model, Prophet (Week 2)

**Goal:** Build the simplest reasonable forecast. Beat this before getting clever.

- [ ] Train/validation/test split (time-based, no random shuffling)
- [ ] Prophet model for solar generation
- [ ] Prophet model for wind generation (onshore + offshore)
- [ ] Baseline evaluation: RMSE, MAE, MAPE
- [ ] Prophet's built-in uncertainty intervals: are they calibrated?
- [ ] Residual analysis: where does the model fail?

**Why Prophet first?**
Prophet handles seasonality, holidays, and trend changepoints with minimal tuning. It provides a credible baseline with uncertainty bands out of the box. If XGBoost outperforms it later, the improvement is meaningful because we compared against something reasonable, not a naive mean.

**Exit criterion:** Working Prophet forecast with documented metrics and failure modes.

---

### Phase 2: Gradient Boosting, XGBoost (Week 3)

**Goal:** Feature-engineered model that captures nonlinear relationships.

- [ ] Feature engineering pipeline (`src/features/engineer.py`)
  - Temporal embeddings (cyclic encoding of hour, day, month)
  - Lag features (24h, 48h, 168h)
  - Rolling statistics
  - Calendar features (weekday vs weekend, German public holidays)
  - Weather covariates (DWD integration)
- [ ] XGBoost training with cross-validation
- [ ] SHAP feature importance analysis: what drives the forecast?
- [ ] Conformal prediction for calibrated uncertainty intervals
- [ ] Comparison with Prophet baseline on all metrics

**Why XGBoost second?**
XGBoost with engineered features often outperforms Prophet because it can use richer input signals. It also integrates naturally with SHAP for explainability, which is critical for operators who need to trust predictions.

**Exit criterion:** XGBoost beats Prophet on at least RMSE and MAE. SHAP analysis identifies top predictive features.

---

### Phase 3: Sequential Model, LSTM (Week 4)

**Goal:** Test whether deep learning adds value on top of classical methods.

- [ ] LSTM architecture design (input window, hidden units, dropout)
- [ ] Training with PyTorch
- [ ] MC Dropout for uncertainty estimation
- [ ] Comparison with XGBoost: honest assessment
- [ ] When does LSTM win? When does it lose?

**Why LSTM third?**
LSTM captures long-range temporal dependencies without manual feature engineering. But it requires more data, more compute, and is harder to interpret. The honest question: does it actually outperform XGBoost here? If XGBoost wins, the results will say so. This project values honesty over narrative.

**Exit criterion:** LSTM trained and evaluated. Clear documentation of when it helps and when it doesn't.

---

### Phase 4: Deployment & Productionization (Week 5)

**Goal:** A working demo with operational infrastructure.

- [ ] Streamlit dashboard
  - Select date range and energy source
  - View forecast with uncertainty bands
  - Compare model outputs side-by-side
  - Show SHAP plot for selected time window
- [ ] FastAPI endpoint for programmatic access (`/predict`)
- [ ] MLflow experiment tracking integrated throughout
- [ ] CI pipeline (GitHub Actions: lint, test, type-check)
- [ ] Docker containerization for reproducible deployment
- [ ] Deploy to Streamlit Cloud or HuggingFace Spaces

**Exit criterion:** Public link to interactive demo. Reproducible from clone to running dashboard.

---

## 6. Model Strategy: Prophet → XGBoost → LSTM

This progression reflects a disciplined modeling philosophy: **start simple, add complexity only when simpler methods fail, and document why.**

### The Comparison Framework

Every model is evaluated on the same held-out test set (2024–2025 data) using:

| Metric | What It Measures | Why It Matters |
|---|---|---|
| **RMSE** | Average error magnitude, penalizes large errors | Grid operators need to avoid large forecast misses |
| **MAE** | Average absolute error | Interpretable in GWh, directly tied to balancing costs |
| **MAPE** | Percentage error | Comparable across different energy sources and scales |
| **Coverage** | % of actuals within prediction interval | Calibration: are the uncertainty bands honest? |
| **Sharpness** | Width of prediction intervals | Tight AND accurate intervals are more useful than wide safe ones |
| **Naive baseline** | Predict tomorrow = today | A model that can't beat this has no operational value |

### Why Uncertainty Metrics Alongside Accuracy

Most tutorials report only RMSE. But an operator does not care that "on average we're off by 1.2 GWh." They care: "If I commit to buying 10 GWh of balancing energy, what is the probability I actually need more than that?"

Prediction intervals answer this, but only if they are **calibrated** (the 80% interval actually contains the truth 80% of the time). This project measures calibration explicitly.

---

## 7. Uncertainty Quantification

In experimental physics, reporting a result without an uncertainty is incomplete science. You don't write "the peak is at 785 nm." You write "785 ± 3 nm (1σ)," and you explain where the uncertainty comes from.

This instinct transfers directly to energy forecasting.

**Three approaches to uncertainty in this project:**

### 7.1 Prophet: Built-in Bayesian Uncertainty

Prophet uses a generative model with uncertainty propagated from trend and seasonality estimates. The intervals come "for free," but they must be validated against actual coverage on the test set. Out-of-the-box Prophet intervals tend to be overconfident.

### 7.2 XGBoost: Conformal Prediction

Conformal prediction is a distribution-free method that converts any point forecast into a statistically valid prediction interval. It guarantees that the 90% interval contains the true value at least 90% of the time, without assumptions about error distribution.

Implementation: calibrate residuals from a validation set, then apply empirical quantiles to test predictions. See `src/uncertainty/conformal.py`.

### 7.3 LSTM: Monte Carlo Dropout

MC Dropout treats dropout layers as approximate Bayesian inference. By keeping dropout active at inference time and running multiple forward passes, we get a distribution of predictions, from which we extract calibrated intervals.

---

## 8. Infrastructure & MLOps

Since this is a forecasting **system** (not just a model), infrastructure design matters. This section documents the operational thinking behind the pipeline.

### 8.1 Data Pipeline

```
SMARD API ──► Rate-limited fetcher ──► Raw JSON cache ──► Parquet (columnar storage)
                  │                         │
                  ▼                         ▼
          Retry logic with           Schema validation
          exponential backoff        (null checks, dtype enforcement,
                                      timestamp continuity)
```

- **Parquet over CSV**: columnar storage, 5-10x compression, native datetime support, schema enforcement
- **Idempotent ingestion**: re-running the pipeline doesn't duplicate data
- **Incremental updates**: fetch only new data since last ingestion timestamp

### 8.2 Experiment Tracking (MLflow)

Every training run logs:
- Hyperparameters
- All evaluation metrics (point forecast + uncertainty)
- Model artifacts
- Data version (date range, feature set hash)
- Training duration and environment info

This makes experiments **reproducible** and **comparable**. No more "which notebook produced that result?"

### 8.3 Testing Strategy

| Layer | What's Tested | Tool |
|---|---|---|
| Data ingestion | API response parsing, schema validation, edge cases (DST, missing hours) | pytest |
| Feature engineering | Correct lag alignment, no future leakage, cyclic encoding range | pytest |
| Models | Training completes, predictions have correct shape, UQ intervals are valid | pytest |
| Integration | End-to-end: raw data → features → prediction → evaluation metrics | pytest |

### 8.4 CI/CD Pipeline (GitHub Actions)

```yaml
on: [push, pull_request]
jobs:
  quality:
    - ruff check (linting)
    - ruff format --check (formatting)
    - pytest tests/ -v (unit + integration tests)
  # Future: automated model validation on data refresh
```

### 8.5 Deployment Architecture (Phase 4)

```
GitHub repo ──► GitHub Actions (CI) ──► Docker image ──► Streamlit Cloud
                                                         or HuggingFace Spaces
                                    ──► FastAPI container ──► /predict endpoint
```

- **Containerized**: Docker ensures "works on my machine" doesn't happen
- **Stateless API**: FastAPI endpoint takes a date range, returns forecast + intervals as JSON
- **Dashboard**: Streamlit for interactive exploration, not production serving

### 8.6 Future Infrastructure Considerations

These are not in scope for the initial build, but documented as next steps:

- **Scheduled retraining**: Cron or Airflow DAG to retrain models weekly on fresh SMARD data
- **Model monitoring**: Track prediction drift over time. Does accuracy degrade as generation patterns shift?
- **Data quality alerts**: Automated checks when SMARD data has unexpected gaps or anomalies
- **A/B model serving**: Route a fraction of predictions to a challenger model for live comparison

---

## 9. Tech Stack & Rationale

Every tool is here for a reason. This is a minimal, purposeful selection.

| Tool | Purpose | Why This and Not X |
|---|---|---|
| **Python 3.11** | Core language | Standard in data science; type hints improve code clarity |
| **SMARD API** | Data ingestion | Official source, mirrors industry workflow |
| **Pandas** | Data manipulation | Ecosystem maturity; Polars as optimization if needed |
| **Prophet** | Baseline forecasting | Interpretable, handles seasonality, built-in UQ |
| **XGBoost** | Main model | Production-proven on tabular time-series; excellent with SHAP |
| **SHAP** | Explainability | Makes models interpretable, necessary for operator trust |
| **PyTorch** | LSTM implementation | Industry standard for deep learning research |
| **MAPIE** | Conformal prediction | Scikit-learn compatible, well-documented |
| **MLflow** | Experiment tracking | Reproducible experiments, model registry |
| **Streamlit** | Demo interface | Fast to deploy, interactive, no frontend expertise needed |
| **FastAPI** | REST API | Async, auto-docs, production-ready |
| **pytest** | Testing | Data pipeline and feature engineering validation |
| **ruff** | Linting & formatting | Fast, replaces flake8 + black + isort |
| **GitHub Actions** | CI pipeline | Auto-run tests and linting on every push |
| **Docker** | Containerization | Reproducible deployment across environments |

**Deliberately excluded (for now):**
- **Airflow/Prefect**: Overkill for a single-pipeline project at this stage
- **Kubernetes**: No need for orchestration until serving at scale
- **Feature store**: Direct feature engineering is sufficient for this scope

---

## 10. Key Design Decisions

These are the choices where I made a judgment call, with the reasoning documented.

### Decision 1: Time-based train/test split, never random

**Chosen approach:** Train on 2018–2023, validate on 2024, test on 2025.

**Why not random split?** Time-series data has temporal structure. A random split lets the model "see the future" during training (data leakage), producing optimistically biased metrics that don't generalize. This is a common mistake this project deliberately avoids.

### Decision 2: Forecast horizon of 24 hours

**Chosen approach:** Predict the next 24 hours from the last known observation.

**Why 24h?** This matches the day-ahead electricity market (EPEX day-ahead auction closes at noon for the next day). It is the operationally relevant horizon. 15-minute resolution is the industry standard; hourly is the starting point here, with sub-hourly as a stretch goal.

### Decision 3: Separate models for solar and wind

**Chosen approach:** Train independent models for solar generation and wind generation.

**Why not a joint model?** Solar and wind have fundamentally different physical drivers (irradiance vs. wind speed), different seasonal profiles, and different time-of-day patterns. A joint model conflates these signals. Separate models are more interpretable and easier to debug and improve independently.

### Decision 4: Evaluate calibration, not just accuracy

**Chosen approach:** Coverage and sharpness metrics alongside RMSE/MAE.

**Why?** An 80% prediction interval that contains the true value only 60% of the time is dangerously misleading. Operators would under-hedge their risk. Calibration is the difference between a forecast and a **reliable** forecast.

### Decision 5: Parquet over CSV for data storage

**Chosen approach:** Store processed data as Parquet files.

**Why?** Parquet provides columnar compression (5-10x smaller files), preserves dtypes (no datetime parsing on every load), and supports schema enforcement. For time-series data with millions of rows, this matters.

---

## 11. Project Structure

```
german-renewable-forecasting/
│
├── data/
│   ├── raw/                    # Raw API responses (git-ignored)
│   ├── processed/              # Cleaned, feature-engineered datasets
│   └── external/               # DWD weather data (Phase 2)
│
├── notebooks/
│   ├── 01_eda.ipynb            # Exploratory Data Analysis
│   ├── 02_prophet_baseline.ipynb
│   ├── 03_xgboost_model.ipynb
│   └── 04_lstm_model.ipynb
│
├── src/
│   ├── data/
│   │   ├── smard_client.py     # SMARD API wrapper
│   │   └── dwd_client.py       # DWD weather data client (Phase 2)
│   ├── features/
│   │   └── engineer.py         # Feature engineering pipeline
│   ├── models/
│   │   ├── prophet_model.py    # Prophet baseline
│   │   ├── xgboost_model.py    # XGBoost + SHAP
│   │   └── lstm_model.py       # LSTM + MC Dropout
│   ├── evaluation/
│   │   └── metrics.py          # RMSE, MAE, MAPE, Coverage, Sharpness
│   └── uncertainty/
│       └── conformal.py        # Conformal prediction intervals
│
├── app/
│   └── streamlit_app.py        # Interactive dashboard
│
├── tests/
│   ├── test_smard_client.py    # Data ingestion tests
│   ├── test_features.py        # Feature engineering tests
│   └── test_metrics.py         # Evaluation metrics tests
│
├── models/
│   └── saved/                  # Trained model artifacts (git-ignored)
│
├── mlruns/                     # MLflow tracking (git-ignored)
│
├── requirements.txt
├── environment.yml
├── .gitignore
├── LICENSE
└── README.md
```

---

## 12. How to Run

### Prerequisites

- Python 3.11+
- Conda or virtualenv

### Setup

```bash
# Clone the repository
git clone https://github.com/Dr-DKP/german-renewable-forecasting.git
cd german-renewable-forecasting

# Create and activate environment
conda env create -f environment.yml
conda activate energy-forecasting

# Or with pip
pip install -r requirements.txt
```

### Fetch Data

```bash
# Download SMARD solar and wind data (2018–2025)
python src/data/smard_client.py --start 2018-01-01 --end 2025-12-31 --source solar wind
```

### Run Notebooks in Order

```bash
jupyter lab
# Open notebooks/ in sequence: 01 → 02 → 03 → 04
```

### Launch Dashboard

```bash
streamlit run app/streamlit_app.py
```

### Run Tests

```bash
pytest tests/ -v
```

### Track Experiments

```bash
mlflow ui
# Open http://localhost:5000
```

---

## 13. Results & Benchmarks

*To be completed as models are trained and validated.*

### Model Comparison Table

| Model | RMSE (GWh) | MAE (GWh) | MAPE (%) | Coverage (80%) | Sharpness |
|---|---|---|---|---|---|
| Naive (24h lag) | - | - | - | - | - |
| Prophet | - | - | - | - | - |
| XGBoost | - | - | - | - | - |
| LSTM | - | - | - | - | - |

> The naive baseline (predict tomorrow = today) is always included. A model that cannot beat it has no operational value.

### Key Findings

*To be updated after each phase completion.*

---

## 14. Lessons Learned

*Updated throughout the project as discoveries are made.*

- **SMARD API quirks:** The API returns data in 15-minute resolution for some endpoints and hourly for others. Alignment requires careful resampling logic.
- **Solar forecasting at night:** Solar generation is exactly zero from ~19:00 to ~06:00 seasonally. Models that don't account for this produce nonsensical overnight predictions. Zero-inflation handling is essential.
- **Prophet calibration:** Prophet's default uncertainty intervals tend to be overconfident (too narrow). Requires tuning `interval_width` and validating coverage empirically.

---

## 15. License & Contact

**MIT License**, see [LICENSE](LICENSE) for details.

**Author:** Dr. Deepak K. Pandey
**Website:** [drdkp.com](https://drdkp.com)
**LinkedIn:** [linkedin.com/in/drdkp](https://linkedin.com/in/drdkp)

---

*Built with genuine interest in renewable energy forecasting and a physicist's instinct for systematic, uncertainty-aware problem solving.*
