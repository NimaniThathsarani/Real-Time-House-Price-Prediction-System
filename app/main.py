from fastapi import FastAPI
import joblib

app = FastAPI()

model = joblib.load("model/model.pkl")

@app.get("/")
def home():
    return {"message": "Food Calorie Advisor API"}

@app.post("/predict")
def predict(data: dict):
    food = data["food"]
    result = model.predict([food])
    return {"calories": result[0]}