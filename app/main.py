from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime


# =====================================
# Load Model
# =====================================

model = joblib.load(
    "models/house_price_model.pkl"
)

# =====================================
# FastAPI App
# =====================================

app = FastAPI(
    title="AI House Price Prediction API"
)

# =====================================
# Logging Setup
# =====================================

os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/prediction_logs.csv"

# =====================================
# Input Schema
# =====================================

class HouseRequest(BaseModel):

    district: str

    area: str

    perch: float

    bedrooms: int

    bathrooms: int

    kitchen_area_sqft: float

    parking_spots: int

    has_garden: bool

    has_ac: bool

    water_supply: str

    electricity: str

    floors: int

    house_age: int


# =====================================
# Root Endpoint
# =====================================

@app.get("/")

def home():

    return {
        "message": "House Price Prediction API Running"
    }

# =====================================
# Prediction Endpoint
# =====================================

@app.post("/predict")

def predict_house_price(request: HouseRequest):

    # =================================
    # Convert input to dataframe
    # =================================

    input_data = pd.DataFrame([{

        "district": request.district,

        "area": request.area,

        "perch": request.perch,

        "bedrooms": request.bedrooms,

        "bathrooms": request.bathrooms,

        "kitchen_area_sqft": request.kitchen_area_sqft,

        "parking_spots": request.parking_spots,

        "has_garden": request.has_garden,

        "has_ac": request.has_ac,

        "water_supply": request.water_supply,

        "electricity": request.electricity,

        "floors": request.floors,

        "house_age": request.house_age
    }])

    # =================================
    # Predict
    # =================================

    prediction = model.predict(input_data)[0]

    predicted_price = round(float(prediction), 2)

    # =================================
    # Price Category
    # =================================

    if predicted_price < 15000000:

        category = "Budget Property"

        insight = "Affordable property with moderate investment value."

    elif predicted_price < 50000000:

        category = "Mid-Range Property"

        insight = "Good residential property with stable market demand."

    else:

        category = "Premium Property"

        insight = "High-value property with strong investment potential."

    # =================================
    # Logging Predictions
    # =================================

    log_data = pd.DataFrame([{

        "district": request.district,

        "area": request.area,

        "bedrooms": request.bedrooms,

        "bathrooms": request.bathrooms,

        "predicted_price": predicted_price,

        "timestamp": datetime.now()
    }])

    if os.path.exists(LOG_FILE):

        log_data.to_csv(
            LOG_FILE,
            mode="a",
            header=False,
            index=False
        )

    else:

        log_data.to_csv(
            LOG_FILE,
            index=False
        )

    # =================================
    # Response
    # =================================

    return {

        "predicted_price_lkr": predicted_price,

        "price_category": category,

        "market_insight": insight
    }