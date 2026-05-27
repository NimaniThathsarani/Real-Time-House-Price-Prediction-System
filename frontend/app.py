import streamlit as st
import requests
 
# =====================================
# Page Config
# =====================================
st.set_page_config(
    page_title="AI House Price Prediction System",
    page_icon="🏠",
    layout="centered"
)
 
# =====================================
# District → Areas Mapping (from dataset)
# =====================================
DISTRICT_AREAS = {
    "Ampara": ["Ampara Central"],
    "Anuradhapura": ["Madawachchiya", "New Town", "Nuwaragam Palatha"],
    "Badulla": ["Badulla Town", "Bandarawela", "Hali Ela"],
    "Batticaloa": ["Batticaloa Town", "Eravur", "Kallady"],
    "Colombo": [
        "Bambalapitiya", "Borella", "Dehiwala", "Kollupitiya",
        "Mount Lavinia", "Narahenpita", "Nugegoda", "Rajagiriya", "Wellawatte"
    ],
    "Galle": ["Galle Fort", "Hikkaduwa", "Karapitiya", "Unawatuna"],
    "Gampaha": ["Gampaha Town", "Ja-Ela", "Kadawatha", "Negombo", "Ragama", "Wattala"],
    "Hambantota": ["Ambalantota", "Hambantota Town", "Tangalle"],
    "Jaffna": ["Chunnakam", "Jaffna Town", "Kokuvil", "Nallur"],
    "Kalutara": ["Beruwala", "Kalutara North", "Panadura", "Wadduwa"],
    "Kandy": ["Gatambe", "Kandy City", "Katugastota", "Peradeniya", "Tennekumbura"],
    "Kegalle": ["Kegalle Central"],
    "Kilinochchi": ["Kilinochchi Central"],
    "Kurunegala": ["Kurunegala Town", "Melsiripura", "Pannala", "Polgahawela"],
    "Mannar": ["Mannar Central"],
    "Matale": ["Matale Central"],
    "Matara": ["Akurugoda", "Matara Town", "Nupe", "Weligama"],
    "Monaragala": ["Monaragala Central"],
    "Mullaitivu": ["Mullaitivu Central"],
    "Nuwara Eliya": ["Nuwara Eliya Central"],
    "Polonnaruwa": ["Polonnaruwa Central"],
    "Puttalam": ["Puttalam Central"],
    "Ratnapura": ["Kuruwita", "Pelmadulla", "Ratnapura Town"],
    "Trincomalee": ["China Bay", "Nilaveli", "Uppuveli"],
    "Vavuniya": ["Vavuniya Central"],
}
 
# =====================================
# Title
# =====================================
st.title("🏠 Real-Time House Price Prediction System")
st.markdown("Predict Sri Lankan house prices using AI.")
 
# =====================================
# User Inputs
# =====================================
district = st.selectbox(
    "District",
    sorted(DISTRICT_AREAS.keys())
)
 
area = st.selectbox(
    "Area",
    DISTRICT_AREAS[district]
)
 
perch = st.number_input(
    "Land Size (Perch)",
    min_value=2.0,
    max_value=80.0,
    value=10.0,
    step=0.5
)
 
bedrooms = st.number_input(
    "Bedrooms",
    min_value=1,
    max_value=7,
    value=3
)
 
bathrooms = st.number_input(
    "Bathrooms",
    min_value=1,
    max_value=5,
    value=2
)
 
kitchen_area_sqft = st.number_input(
    "Kitchen Area (sqft)",
    min_value=35.0,
    max_value=250.0,
    value=120.0,
    step=5.0
)
 
parking_spots = st.number_input(
    "Parking Spots",
    min_value=0,
    max_value=3,
    value=1
)
 
floors = st.number_input(
    "Floors",
    min_value=1,
    max_value=3,
    value=2
)
 
house_age = st.number_input(
    "House Age (years)",
    min_value=1,
    max_value=41,
    value=5
)
 
has_garden = st.checkbox("Has Garden")
has_ac = st.checkbox("Has AC")
 
water_supply = st.selectbox(
    "Water Supply",
    ["Pipe-borne", "Well", "Both"]
)
 
electricity = st.selectbox(
    "Electricity",
    ["Single phase", "Three phase"]
)
 
# =====================================
# Prediction Button
# =====================================
if st.button("Predict House Price"):
    payload = {
        "district": district,
        "area": area,
        "perch": perch,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "kitchen_area_sqft": kitchen_area_sqft,
        "parking_spots": parking_spots,
        "has_garden": has_garden,
        "has_ac": has_ac,
        "water_supply": water_supply,
        "electricity": electricity,
        "floors": floors,
        "house_age": house_age,
    }
 
    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=payload
        )
        result = response.json()
 
        st.success("Prediction Completed!")
 
        st.subheader("💰 Predicted House Price")
        st.write(f"LKR {result['predicted_price_lkr']:,.2f}")
 
        st.subheader("🏷 Property Category")
        st.write(result["price_category"])
 
        st.subheader("📈 Market Insight")
        st.write(result["market_insight"])
 
    except Exception as e:
        st.error(f"Error: {e}")