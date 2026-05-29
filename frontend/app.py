import streamlit as st
import requests
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# =====================================
# Page Config & Title styling
# =====================================
st.set_page_config(
    page_title="Sri Lankan House Valuation AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject FontAwesome and Custom Vanilla CSS (Light Mode layout)
st.markdown("""
<!-- Load FontAwesome -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
    /* Import Outfit font */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    /* Global style resets and overrides */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Outfit', sans-serif !important;
        background: radial-gradient(circle at 10% 20%, #f8fafc 0%, #f1f5f9 100%) !important;
        color: #334155 !important;
    }
    
    /* Subheader & Subtitle customizations */
    .app-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 15px;
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
    }
    .app-subtitle {
        font-size: 1.1rem;
        color: #64748b;
        margin-bottom: 2rem;
    }

    /* Container blocks styled as clean white elevation cards */
    .glass-card {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.05) !important;
    }

    /* Target standard Streamlit Expander to match style */
    div[data-testid="stExpander"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03) !important;
    }
    div[data-testid="stExpander"] > details > summary {
        font-weight: 600 !important;
        color: #0f172a !important;
        font-size: 15px !important;
    }

    /* Custom Metric Cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 12px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
        margin: 5px 0;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #0f172a;
        margin-top: 4px;
    }
    .metric-label {
        font-size: 11px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
    }

    /* Custom Badges */
    .badge-budget {
        background-color: rgba(16, 185, 129, 0.1);
        color: #047857;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 12px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 13px;
        display: inline-block;
    }
    .badge-mid {
        background-color: rgba(59, 130, 246, 0.1);
        color: #1d4ed8;
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 4px 12px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 13px;
        display: inline-block;
    }
    .badge-premium {
        background-color: rgba(245, 158, 11, 0.1);
        color: #b45309;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 4px 12px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 13px;
        display: inline-block;
    }

    /* Style primary submit buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 12px 28px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45) !important;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    }
    div.stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* Tabs Styling */
    button[data-baseweb="tab"] {
        font-family: 'Outfit', sans-serif !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #64748b !important;
        background-color: transparent !important;
        border: none !important;
        padding: 14px 20px !important;
        transition: all 0.2s ease !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #1d4ed8 !important;
        border-bottom: 3px solid #2563eb !important;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# District → Areas Mapping
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

LOG_FILE = "logs/prediction_logs.csv"

# =====================================
# Cached Loaders
# =====================================
@st.cache_resource
def load_local_model():
    paths = ["models/house_price_model.pkl", "../models/house_price_model.pkl"]
    for p in paths:
        if os.path.exists(p):
            try:
                return joblib.load(p)
            except Exception:
                pass
    return None

@st.cache_data
def load_market_data():
    paths = [
        "data/processed/cleaned_house_data.csv",
        "cleaned_house_data.csv",
        "../data/processed/cleaned_house_data.csv"
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return pd.read_csv(p)
            except Exception:
                pass
    return None

def load_prediction_logs():
    if os.path.exists(LOG_FILE):
        try:
            return pd.read_csv(LOG_FILE)
        except Exception:
            return None
    return None

# =====================================
# Main Header Layout
# =====================================
st.markdown('<div class="app-title"><i class="fa-solid fa-house-laptop" style="margin-right: 15px; color: #2563eb;"></i> Sri Lankan House Valuation AI</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Real-time property appraisal engine powered by Machine Learning & MLOps</div>', unsafe_allow_html=True)

# API Endpoint URL
api_url = "http://127.0.0.1:8000/predict"

# Set up tabs
tab1, tab2, tab3 = st.tabs(["AI Price Predictor", "Market Analytics", "Valuation Log"])

# =====================================
# Tab 1: AI Predictor
# =====================================
with tab1:
    col_inputs, col_results = st.columns([1.3, 1.0])
    
    with col_inputs:
        st.markdown('### Property Specifications')
        
        # 1. Location details
        with st.expander("Location & District", expanded=True):
            col_loc1, col_loc2 = st.columns(2)
            with col_loc1:
                district = st.selectbox("District", sorted(DISTRICT_AREAS.keys()), key="pred_district")
            with col_loc2:
                area = st.selectbox("Area", DISTRICT_AREAS[district], key="pred_area")
                
        # 2. Dimensions and configurations
        with st.expander("Dimensions & Configuration", expanded=True):
            col_dim1, col_dim2 = st.columns(2)
            with col_dim1:
                perch = st.number_input("Land Size (Perch)", min_value=2.0, max_value=80.0, value=10.0, step=0.5, help="Total land extent in perches (1 Perch ≈ 272 sqft)")
                bedrooms = st.number_input("Bedrooms", min_value=1, max_value=7, value=3, step=1, help="Total bedrooms in the house")
                floors = st.number_input("Floors", min_value=1, max_value=3, value=2, step=1, help="Number of storeys")
            with col_dim2:
                kitchen_area_sqft = st.number_input("Kitchen Area (sqft)", min_value=35.0, max_value=250.0, value=120.0, step=5.0, help="Approximate kitchen area in square feet")
                bathrooms = st.number_input("Bathrooms", min_value=1, max_value=5, value=2, step=1, help="Total bathrooms in the house")
                house_age = st.number_input("House Age (years)", min_value=1, max_value=41, value=5, step=1, help="Years elapsed since house construction")

        # 3. Utilities & Features
        with st.expander("Utilities & Additional Features", expanded=True):
            col_ut1, col_ut2 = st.columns(2)
            with col_ut1:
                water_supply = st.selectbox("Water Supply Source", ["Pipe-borne", "Well", "Both"])
                electricity = st.selectbox("Electricity Setup", ["Single phase", "Three phase"])
            with col_ut2:
                parking_spots = st.number_input("Parking Spaces", min_value=0, max_value=3, value=1, step=1, help="Number of dedicated parking slots")
            
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            col_chk1, col_chk2 = st.columns(2)
            with col_chk1:
                has_garden = st.checkbox("Has Garden", value=True)
            with col_chk2:
                has_ac = st.checkbox("Has Air Conditioning (AC)", value=False)
                
        st.markdown("<br>", unsafe_allow_html=True)
        predict_btn = st.button("Calculate Property Value", use_container_width=True)

    with col_results:
        st.markdown('### Valuation Summary')
        
        if predict_btn:
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
            
            predicted_price = None
            category = ""
            insight = ""
            
            # Prediction Inference block
            with st.spinner("Analyzing house features..."):
                try:
                    response = requests.post(api_url, json=payload, timeout=2.5)
                    if response.status_code == 200:
                        result = response.json()
                        predicted_price = result["predicted_price_lkr"]
                        category = result["price_category"]
                        insight = result["market_insight"]
                except Exception:
                    pass
                
                # Local Inference Fallback (Silent failover)
                if predicted_price is None:
                    local_model = load_local_model()
                    if local_model is not None:
                        try:
                            # Reconstruct DataFrame matching pipeline columns
                            input_df = pd.DataFrame([payload])
                            prediction = local_model.predict(input_df)[0]
                            predicted_price = round(float(prediction), 2)
                            
                            # Local threshold classifications
                            if predicted_price < 15000000:
                                category = "Budget Property"
                                insight = "Affordable property with moderate investment value."
                            elif predicted_price < 50000000:
                                category = "Mid-Range Property"
                                insight = "Good residential property with stable market demand."
                            else:
                                category = "Premium Property"
                                insight = "High-value property with strong investment potential."
                                
                            # Manually append to prediction logs csv (MLOps local logger)
                            os.makedirs("logs", exist_ok=True)
                            log_data = pd.DataFrame([{
                                "district": district,
                                "area": area,
                                "bedrooms": bedrooms,
                                "bathrooms": bathrooms,
                                "predicted_price": predicted_price,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                            }])
                            if os.path.exists(LOG_FILE):
                                log_data.to_csv(LOG_FILE, mode="a", header=False, index=False)
                            else:
                                log_data.to_csv(LOG_FILE, index=False)
                        except Exception as local_err:
                            st.error(f"Inference pipeline error: {local_err}")
                    else:
                        st.error("Valuation service unavailable. Please check your backend api connection.")
            
            if predicted_price is not None:
                # USD Conversion estimate (using a realistic rate of 1 USD ≈ 300 LKR)
                usd_price = predicted_price / 300.0
                
                # Pick badge class
                if category == "Premium Property":
                    badge_html = f'<span class="badge-premium">{category}</span>'
                elif category == "Mid-Range Property":
                    badge_html = f'<span class="badge-mid">{category}</span>'
                else:
                    badge_html = f'<span class="badge-budget">{category}</span>'
                
                # Elegant output layout card
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color:#64748b; font-size:11px; text-transform:uppercase; letter-spacing:0.08em;"><i class="fa-solid fa-coins" style="margin-right: 4px; color: #2563eb;"></i> Estimated Value</span>
                    </div>
                    <div style="margin: 8px 0;">
                        <h1 style="margin:0; font-size:42px; font-weight:800; color:#0f172a; line-height:1.1;">LKR {predicted_price:,.2f}</h1>
                        <p style="margin:4px 0 0 0; color:#2563eb; font-size:18px; font-weight:600;">≈ ${usd_price:,.0f} USD <span style="font-size:11px; font-weight:normal; color:#64748b;">(1 USD = 300 LKR)</span></p>
                    </div>
                    <hr style="border:0; border-top:1px solid #e2e8f0; margin:16px 0;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <span style="color:#64748b; font-size:14px;"><i class="fa-solid fa-ranking-star" style="margin-right: 5px; color: #2563eb;"></i> Market Classification:</span>
                        {badge_html}
                    </div>
                    <div style="color:#334155; font-size:14px; line-height:1.5; background:#f8fafc; padding:14px; border-radius:8px; border:1px solid #e2e8f0;">
                        <strong><i class="fa-solid fa-lightbulb" style="color:#b45309; margin-right: 6px;"></i> Market Insight:</strong><br>{insight}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Check for historical processed data to plot percentile gauge
                market_df = load_market_data()
                if market_df is not None:
                    # Filter
                    area_data = market_df[market_df["area"] == area]
                    ref_name = f"Area: {area}"
                    if area_data.empty:
                        area_data = market_df[market_df["district"] == district]
                        ref_name = f"District: {district}"
                        
                    if not area_data.empty:
                        prices = area_data["price_lkr"]
                        min_val = float(prices.min())
                        max_val = float(prices.max())
                        med_val = float(prices.median())
                        
                        # Percentile rank
                        pct_rank = (prices < predicted_price).mean() * 100
                        
                        # Render gauge (configured with dark text colors for light background)
                        fig_gauge = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=predicted_price,
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': f"Valuation Position relative to {ref_name}", 'font': {'size': 13, 'color': '#475569', 'family': 'Outfit'}},
                            number={'font': {'color': '#0f172a', 'size': 18, 'family': 'Outfit'}, 'prefix': "LKR ", 'valueformat': ",.0f"},
                            gauge={
                                'axis': {'range': [min_val, max_val], 'tickcolor': '#64748b', 'tickfont': {'size': 10, 'color': '#475569'}},
                                'bar': {'color': '#2563eb'},
                                'bgcolor': '#f8fafc',
                                'borderwidth': 1,
                                'bordercolor': '#cbd5e1',
                                'steps': [
                                    {'range': [min_val, med_val], 'color': 'rgba(16, 185, 129, 0.08)'},
                                    {'range': [med_val, max_val], 'color': 'rgba(245, 158, 11, 0.08)'}
                                ],
                                'threshold': {
                                    'line': {'color': '#ef4444', 'width': 3},
                                    'thickness': 0.75,
                                    'value': med_val
                                }
                            }
                        ))
                        fig_gauge.update_layout(
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font={'color': '#334155'},
                            height=190,
                            margin=dict(l=15, r=15, t=35, b=10)
                        )
                        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
                        
                        st.markdown(f"""
                        <div style='text-align:center; font-size:13px; color:#64748b; margin-top:-5px;'>
                            This valuation is higher than <strong>{pct_rank:.1f}%</strong> of sampled properties in this locality.<br>
                            <span style='color:#ef4444; font-size:14px; margin-right:4px;'>▬</span> Median local price: LKR {med_val:,.0f}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Additional local dataset statistics could not be loaded. Please run the training pipeline to generate standard CSV data.")
        else:
            # Welcome card
            st.markdown("""
            <div style="text-align:center; padding:90px 30px; border:2px dashed #cbd5e1; border-radius:16px; background:#ffffff;">
                <div style="margin-bottom: 20px;">
                    <i class="fa-solid fa-calculator" style="font-size: 60px; color: #2563eb; opacity: 0.8; filter: drop-shadow(0 4px 10px rgba(37, 99, 235, 0.15));"></i>
                </div>
                <h3 style="color:#0f172a; font-size:20px; margin-bottom:8px; font-weight:700;">Awaiting Appraisal</h3>
                <p style="color:#64748b; font-size:14px; line-height:1.6; max-width:320px; margin:0 auto;">
                    Adjust the property specifications in the left panel and click <strong>Calculate Property Value</strong> to query the AI predictor.
                </p>
            </div>
            """, unsafe_allow_html=True)

# =====================================
# Tab 2: Market Analytics
# =====================================
with tab2:
    market_df = load_market_data()
    if market_df is not None:
        st.markdown("### Market Valuation Insights")
        st.markdown("Explore distribution curves, correlations, and feature drivers of Sri Lankan properties based on the core dataset.")
        
        # Select Filters
        col_sel1, col_sel2 = st.columns(2)
        with col_sel1:
            dist_filter = st.selectbox("Select District for Analysis", ["All Districts"] + sorted(list(market_df["district"].unique())), key="ana_district")
        with col_sel2:
            if dist_filter == "All Districts":
                area_filter = "All Areas"
                st.selectbox("Select Area for Analysis", ["All Areas"], disabled=True, key="ana_area")
            else:
                areas_in_dist = sorted(list(market_df[market_df["district"] == dist_filter]["area"].unique()))
                area_filter = st.selectbox("Select Area for Analysis", ["All Areas"] + areas_in_dist, key="ana_area")
                
        # Filter dataframe
        filtered_df = market_df.copy()
        title_suffix = "Sri Lanka"
        if dist_filter != "All Districts":
            filtered_df = filtered_df[filtered_df["district"] == dist_filter]
            title_suffix = dist_filter
            if area_filter != "All Areas":
                filtered_df = filtered_df[filtered_df["area"] == area_filter]
                title_suffix = f"{area_filter}, {dist_filter}"
                
        # Compute summary metrics
        total_props = len(filtered_df)
        avg_price = filtered_df["price_lkr"].mean() if total_props > 0 else 0
        avg_perch = filtered_df["perch"].mean() if total_props > 0 else 0
        avg_price_perch = avg_price / avg_perch if avg_perch > 0 else 0
        median_price = filtered_df["price_lkr"].median() if total_props > 0 else 0
        
        # Display Metrics Cards
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label"><i class="fa-solid fa-database" style="color: #2563eb;"></i> Sample Count</div>
                <div class="metric-value">{total_props:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label"><i class="fa-solid fa-money-bill-trend-up" style="color: #10b981;"></i> Average Valuation</div>
                <div class="metric-value">LKR {avg_price/1e6:.2f}M</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label"><i class="fa-solid fa-scale-balanced" style="color: #6366f1;"></i> Median Valuation</div>
                <div class="metric-value">LKR {median_price/1e6:.2f}M</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label"><i class="fa-solid fa-chart-area" style="color: #f59e0b;"></i> Avg Price / Perch</div>
                <div class="metric-value">LKR {avg_price_perch/1e6:.2f}M</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
        
        # Row 1 of Charts
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            # Price Distribution histogram
            fig_hist = px.histogram(
                filtered_df, 
                x="price_lkr", 
                nbins=35,
                title=f"Price Distribution Curve ({title_suffix})",
                labels={"price_lkr": "Price (LKR)"},
                color_discrete_sequence=["#2563eb"]
            )
            fig_hist.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': "#334155", 'family': "Outfit"},
                height=320,
                xaxis={'gridcolor': '#e2e8f0', 'title': "Valuation (LKR)", 'title_font': {'color': '#334155'}},
                yaxis={'gridcolor': '#e2e8f0', 'title': "Property Count", 'title_font': {'color': '#334155'}},
                margin=dict(l=40, r=20, t=50, b=40)
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            
        with col_c2:
            # Land Size vs Price Scatter
            fig_scatter = px.scatter(
                filtered_df,
                x="perch",
                y="price_lkr",
                color="bedrooms",
                title=f"Land Size (Perches) vs Price ({title_suffix})",
                labels={"perch": "Land Size (Perch)", "price_lkr": "Price (LKR)", "bedrooms": "Bedrooms"},
                color_continuous_scale="Turbo"
            )
            fig_scatter.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': "#334155", 'family': "Outfit"},
                height=320,
                xaxis={'gridcolor': '#e2e8f0', 'title_font': {'color': '#334155'}},
                yaxis={'gridcolor': '#e2e8f0', 'title_font': {'color': '#334155'}},
                margin=dict(l=40, r=20, t=50, b=40)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        # Row 2: Premium Features Impact
        st.markdown("### Premium Price Appreciators Analysis")
        col_feat1, col_feat2 = st.columns(2)
        
        with col_feat1:
            if "has_garden" in filtered_df.columns:
                garden_stats = filtered_df.groupby("has_garden")["price_lkr"].mean().reset_index()
                garden_stats["has_garden"] = garden_stats["has_garden"].map({True: "With Garden", False: "No Garden"})
                fig_garden = px.bar(
                    garden_stats,
                    x="has_garden",
                    y="price_lkr",
                    title="Average Price: Garden Premium",
                    labels={"has_garden": "Garden Access", "price_lkr": "Avg Price (LKR)"},
                    color="has_garden",
                    color_discrete_map={"With Garden": "#10b981", "No Garden": "#ef4444"}
                )
                fig_garden.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': "#334155", 'family': "Outfit"},
                    height=260,
                    showlegend=False,
                    xaxis={'title': ""},
                    yaxis={'gridcolor': '#e2e8f0', 'title': "Avg Price (LKR)", 'title_font': {'color': '#334155'}},
                    margin=dict(l=40, r=20, t=50, b=40)
                )
                st.plotly_chart(fig_garden, use_container_width=True)
                
        with col_feat2:
            if "has_ac" in filtered_df.columns:
                ac_stats = filtered_df.groupby("has_ac")["price_lkr"].mean().reset_index()
                ac_stats["has_ac"] = ac_stats["has_ac"].map({True: "Air Conditioned", False: "Standard"})
                fig_ac = px.bar(
                    ac_stats,
                    x="has_ac",
                    y="price_lkr",
                    title="Average Price: Climate Control (AC) Premium",
                    labels={"has_ac": "AC Availability", "price_lkr": "Avg Price (LKR)"},
                    color="has_ac",
                    color_discrete_map={"Air Conditioned": "#2563eb", "Standard": "#f59e0b"}
                )
                fig_ac.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': "#334155", 'family': "Outfit"},
                    height=260,
                    showlegend=False,
                    xaxis={'title': ""},
                    yaxis={'gridcolor': '#e2e8f0', 'title': "Avg Price (LKR)", 'title_font': {'color': '#334155'}},
                    margin=dict(l=40, r=20, t=50, b=40)
                )
                st.plotly_chart(fig_ac, use_container_width=True)
    else:
        st.info("Market analytics is unavailable because processed data is missing. Place cleaned_house_data.csv in data/processed/ to enable dashboard.")

# =====================================
# Tab 3: History & Logs
# =====================================
with tab3:
    log_df = load_prediction_logs()
    if log_df is not None and not log_df.empty:
        st.markdown("### System Prediction Audit Log")
        st.markdown("Monitor history logs of real-time property valuation queries run by the prediction API.")
        
        # Display Logs Summary Stats
        log_cnt = len(log_df)
        log_avg = log_df["predicted_price"].mean() if "predicted_price" in log_df.columns else 0
        log_top_district = log_df["district"].mode().iloc[0] if "district" in log_df.columns and len(log_df["district"]) > 0 else "N/A"
        
        col_l1, col_l2, col_l3 = st.columns(3)
        with col_l1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label"><i class="fa-solid fa-list-check" style="color: #2563eb;"></i> Queries Logged</div>
                <div class="metric-value">{log_cnt}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_l2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label"><i class="fa-solid fa-map-location-dot" style="color: #6366f1;"></i> Most Searched District</div>
                <div class="metric-value" style="font-size: 20px; line-height: 2.2; color: #0f172a; font-weight: 700;">{log_top_district}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_l3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label"><i class="fa-solid fa-hand-holding-dollar" style="color: #10b981;"></i> Average Appraised Price</div>
                <div class="metric-value">LKR {log_avg/1e6:.2f}M</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
        
        # Render a line plot of predicted prices over time
        if "timestamp" in log_df.columns:
            try:
                log_df_chart = log_df.copy()
                log_df_chart["timestamp"] = pd.to_datetime(log_df_chart["timestamp"])
                log_df_chart = log_df_chart.sort_values("timestamp")
                
                fig_trend = px.line(
                    log_df_chart,
                    x="timestamp",
                    y="predicted_price",
                    title="Real-Time Valuation Request Value Trend",
                    labels={"timestamp": "Appraisal Timestamp", "predicted_price": "Predicted Price (LKR)"},
                    markers=True
                )
                fig_trend.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': "#334155", 'family': "Outfit"},
                    height=280,
                    xaxis={'gridcolor': '#e2e8f0', 'title_font': {'color': '#334155'}},
                    yaxis={'gridcolor': '#e2e8f0', 'title_font': {'color': '#334155'}},
                    margin=dict(l=40, r=20, t=50, b=40)
                )
                st.plotly_chart(fig_trend, use_container_width=True)
            except Exception as trend_err:
                pass
                
        st.markdown("#### Searchable History Logs Table")
        
        # Filter/Format logs dataframe
        styled_log_df = log_df.copy()
        if "timestamp" in styled_log_df.columns:
            try:
                styled_log_df["timestamp"] = pd.to_datetime(styled_log_df["timestamp"]).dt.strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                pass
                
        # Reorder columns to look clean
        cols_ordered = ["timestamp", "district", "area", "bedrooms", "bathrooms", "predicted_price"]
        existing_cols = [c for c in cols_ordered if c in styled_log_df.columns]
        styled_log_df = styled_log_df[existing_cols]
        
        st.dataframe(
            styled_log_df.style.format({"predicted_price": "LKR {:,.2f}"}),
            use_container_width=True
        )
    else:
        st.info("No prediction logs have been created yet. Run predictions in Tab 1 to generate audit files.")