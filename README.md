# US Visa Approval Prediction

A machine learning project that predicts US visa approval (case status) using a modular MLOps-style pipeline. The project includes data ingestion from MongoDB, data validation (drift detection), data transformation, model training, evaluation, and a prediction endpoint served with FastAPI and a simple Jinja2 web UI.

## Quick overview
- Predicts visa `case_status` from applicant/employer features.
- Modular pipeline: ingestion → validation → transformation → training → evaluation → push → predict.
- Simple web UI (Jinja2) + FastAPI endpoints.

## Key Features
- MLOps-style modular pipeline:
  - Data ingestion from MongoDB
  - Schema-based data validation and drift detection (Evidently)
  - Data transformation and feature engineering
  - Model training, evaluation and model pusher
- Simple web UI (Jinja2) for manual prediction
- FastAPI-based endpoints to trigger training and predict
- Docker-ready for containerized deployment
- Notebook(s) for EDA and local experiments

## Tech stack
- Python 3.8
- FastAPI, Uvicorn (API)
- pandas, numpy (data)
- scikit-learn (models, preprocessing)
- Evidently (data drift)
- MongoDB (data source)
- AWS S3 / ECR (optional model/artifact storage)
- Docker (containerization)
- Jinja2 + Bootstrap (frontend)

## Pipeline (high level)
1. Data Ingestion: read from MongoDB → feature-store CSV (us_visa/components/data_ingestion.py)  
2. Data Validation: schema checks + drift report (Evidently)  
3. Data Transformation: encoders/scalers → save `preprocessing.pkl`  
4. Model Training: train & save `model.pkl`  
5. Model Evaluation & Pusher: compare, accept and push to storage (S3/ECR)  
6. Prediction: load artifacts and serve via FastAPI (`app.py` and `us_visa/pipelines/prediction_pipeline.py`)

## Quick start
- With Docker:
  - Build: `docker build -t us-visa-predictor .`
  - Run: `docker run -p 8000:8000 --env-file .env us-visa-predictor`
- Locally:
  - Create venv, install: `pip install -r requirements.txt`
  - Run: `python app.py` or `uvicorn app:app --reload`

## Endpoints
- GET `/` — web form
- GET `/train` — trigger full training pipeline
- POST `/` — submit form to get a prediction

## Required env vars (example)
- MONGODB_URL (MongoDB connection string)
- AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY (if using S3/ECR)
- APP_HOST, APP_PORT

## Repo pointers
- app.py — API + UI
- us_visa/components — ingestion, validation, transformation, trainer
- us_visa/pipelines — training_pipeline.py, prediction_pipeline.py
- templates/usvisa.html — UI
