# Real-Time House Price Prediction System

An end-to-end Machine Learning and MLOps project that predicts residential property prices in Sri Lanka using a Random Forest Regression model. The system integrates data preprocessing, machine learning model training, FastAPI backend development, Docker containerization, CI/CD workflows and prediction logging into a production-style deployment pipeline.

---

# Features

* Real-time house price prediction
* FastAPI REST API backend
* Machine Learning prediction pipeline
* Data preprocessing & feature engineering
* Dockerized application
* GitHub Actions CI workflow
* Prediction logging & monitoring
* Swagger API documentation

---

# Technology Stack

* Python 3.11
* Scikit-learn
* Pandas
* NumPy
* FastAPI
* Uvicorn
* Docker
* GitHub Actions

---

# Project Structure

```text
Real-Time-House-Price-Prediction-System/
│
├── .github/workflows/      # CI workflow
├── app/                    # FastAPI backend
├── data/                   # Dataset files
├── frontend/               # Streamlit Frontend
├── logs/                   # Prediction logs
├── models/                 # Trained ML model
├── notebooks/              # Training notebooks
├── Dockerfile              # Docker configuration
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/NimaniThathsarani/Real-Time-House-Price-Prediction-System.git
cd Real-Time-House-Price-Prediction-System
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Docker Usage

Build Docker image:

```bash
docker build -t house-price-api .
```

Run Docker container:

```bash
docker run -p 8000:8000 house-price-api
```

Access API:

```text
http://localhost:8000/docs
```

---

# API Endpoint

## POST /predict

Predicts house prices based on property features.

Example response:

```json
{
  "predicted_price_lkr": 38639118.17,
  "price_category": "Mid-Range Property",
  "market_insight": "Good residential property with stable market demand."
}
```

---

# Machine Learning Model

* Algorithm: Random Forest Regressor
* Framework: Scikit-learn Pipeline
* Evaluation Metrics:

  * MAE
  * RMSE
  * R² Score

---

# Dataset

Dataset Source:
https://www.kaggle.com/datasets/dewminimnaadi/house-prices-in-sri-lanka

---

# CI/CD

The project includes GitHub Actions workflow automation for Continuous Integration (CI) to validate dependencies and application configuration automatically on every push.
