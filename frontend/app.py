import streamlit as st
import requests

st.title("🍽️ Food Calorie Advisor")

food = st.text_input("Enter food")

if st.button("Predict"):
    res = requests.post(
        "http://127.0.0.1:8000/predict",
        json={"food": food}
    )
    st.write(res.json())