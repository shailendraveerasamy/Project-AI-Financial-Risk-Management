import streamlit as st
import requests
from datetime import datetime
# --------------------------
# Page config
# --------------------------
st.set_page_config(
    page_title="Fraud Detection Demo",
    page_icon=":kreditkarte:",
    layout="wide"
)
# --------------------------
# Basic styling (CSS)
# --------------------------
st.markdown("""
<style>
/* :weißes_häkchen: Light, clean background */
.stApp {
    background: radial-gradient(circle at top left, #FFFFFF 0%, #F8FAFC 40%, #E5E7EB 100%);
}
/* :weißes_häkchen: White content card */
.block-container {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}
/* :weißes_häkchen: Title styling */
h1, h2, h3 {
    font-weight: 700;
    color: #111827;
}
/* :weißes_häkchen: Normal text */
p, label, span {
    color: #374151;
}
/* :weißes_häkchen: Sleeker number + text inputs */
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    border-radius: 10px;
    background-color: #F9FAFB;
}
/* :weißes_häkchen: Full-width primary button */
div[data-testid="baseButton-secondary"],
div[data-testid="baseButton-primary"] {
    width: 100%;
    border-radius: 12px;
}
/* Fix text colour inside st.text_input */
.stTextInput input {
    color: #111827 !important;         /* dark text */
    background-color: #F9FAFB !important;
}
/* Fix placeholder colour */
.stTextInput input::placeholder {
    color: #6B7280 !important;         /* subtle gray */
}
/* Force headings to be dark */
h1, h2, h3, h4, h5, h6,
.block-container h1,
.block-container h2,
.block-container h3,
.block-container h4,
.block-container h5,
.block-container h6 {
    color: #111827 !important;   /* <- dark gray */
}
/* Streamlit sometimes renders markdown headers as <p> tags */
.block-container p strong,
.block-container p em,
.block-container p {
    color: #111827 !important;
}
</style>
""", unsafe_allow_html=True)
# --------------------------
# Sidebar
# --------------------------
with st.sidebar:
    st.subheader(":kreditkarte: About this demo")
    st.write(
        "This app sends transaction features to a fraud detection model "
        "and returns the **likelihood of credit card fraud**."
    )
    st.markdown("---")
    st.caption("Enter the features on the right and click **Predict Fraud Score**.")
# --------------------------
# Header
# --------------------------
st.markdown("## :kreditkarte: Fraud Detection Demo")
st.markdown(
    """
    Use this demo to estimate the **likelihood that a given credit card transaction is fraudulent**
    based on its amount and other transaction features.
    """
)
st.markdown("---")
# --------------------------
# Backend URL
# --------------------------
#url = "http://127.0.0.1:8000/predict_new"
url = "https://fraud-app-546443544540.europe-west1.run.app/predict_new"

# --------------------------
# Predefined locations (user-friendly → coordinates)
# --------------------------
CARDHOLDER_LOCATIONS = {
    "Berlin, DE": {"lat": 52.5200, "long": 13.4050},
    "Paris, FR": {"lat": 48.8566, "long": 2.3522},
    "New York, US": {"lat": 40.7128, "long": -74.0060},
    "San Francisco, US": {"lat": 37.7749, "long": -122.4194},
}
MERCHANT_LOCATIONS = {
    "Online Store (EU)": {"lat": 50.1109, "long": 8.6821},   # e.g. Frankfurt
    "Berlin Shop": {"lat": 52.5200, "long": 13.4050},
    "Munich Shop": {"lat": 48.1351, "long": 11.5820},
    "Paris Boutique": {"lat": 48.8566, "long": 2.3522},
}

    # Transaction amount
    amt = st.number_input("💰 Amount", format="%.6f", min_value=0.0, value=10000.0)

# --------------------------
# Category options
# --------------------------
CATEGORY_MAP = {
    "misc_net": "Miscellaneous (Online)",
    "misc_pos": "Miscellaneous (In-Store)",
    "entertainment": "Entertainment",
    "gas_transport": "Gas & Transport",
    "grocery_pos": "Groceries (In-Store)",
    "grocery_net": "Grocery (Online)",
    "shopping_net": "Shopping (Online)",
    "shopping_pos": "Shopping (In-Store)",
    "food_dining": "Food & Dining",
    "personal_care": "Personal Care",
    "health_fitness": "Health & Fitness",
    "travel": "Travel",
    "kids_pets": "Kids & Pets",
    "home": "Home",
}

CATEGORY_OPTIONS = list(CATEGORY_MAP.values())
REVERSE_CATEGORY_MAP = {v: k for k, v in CATEGORY_MAP.items()}


# --------------------------
# Input form
# --------------------------
with st.form("fraud_form"):
    # Transaction amount
    amt = st.number_input(":geldsack: Amount", format="%.6f", min_value=0.0, value=10000.0)
    st.markdown("### :1234: Transaction Features")
    feature_config = {
        "Transaction date/ time": {"type": "datetime"},
        "Category": {"type": "select", "options": CATEGORY_OPTIONS},
        "Gender": {"type": "select", "options": ["Male", "Female", "Other"]},
        "Date of Birth": {"type": "date"},
    }
    features = {}
    cols = st.columns(4)  # 4-column grid
    for idx, (feature, config) in enumerate(feature_config.items()):
        col = cols[idx % 4]
        with col:
            if config["type"] == "select":
                features[feature] = st.selectbox(
                    feature,
                    config["options"],
                    key=feature
                )
            elif config["type"] == "datetime":
                features[feature] = st.datetime_input(
                    feature,
                    value=datetime.now(),
                    key=feature
                )
            elif config["type"] == "date":
                features[feature] = st.date_input(
                    feature,
                    value=datetime(1990, 1, 1),
                    min_value=datetime(1920, 1, 1),   # lower bound for DOB
                    max_value=datetime(2026, 1, 1),   # upper bound for DOB
                    key=feature
                )
    st.markdown("### :runde_reißzwecke: Locations")
    col_loc1, col_loc2 = st.columns(2)
    with col_loc1:
        cardholder_location = st.selectbox(
            "Cardholder location",
            list(CARDHOLDER_LOCATIONS.keys()),
            key="cardholder_location"
        )
    with col_loc2:
        merchant_location = st.selectbox(
            "Merchant location",
            list(MERCHANT_LOCATIONS.keys()),
            key="merchant_location"
        )
    # Optional: show what is actually sent to the model
    with st.expander("Advanced (optional): coordinates used for the model"):
        st.write("These values are sent to the model, but you don't need to edit them.")
        st.json({
            "cardholder": CARDHOLDER_LOCATIONS[cardholder_location],
            "merchant": MERCHANT_LOCATIONS[merchant_location],
        })
    # Submit button
    st.markdown(" ")
    submit = st.form_submit_button(":lupe: Predict Fraud Score")
# --------------------------
# Prediction logic
# --------------------------
if submit:
    # Extract and format values for API
    trans_dt = features["Transaction date/ time"]
    dob = features["Date of Birth"]

    params = {
        "trans_date_trans_time": trans_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "category": features["Category"],
        "amt": amt,
        "gender": features["Gender"],
        "lat": features["Lat (Cardholder)"],
        "long": features["Long (Cardholder)"],
        "dob": dob.strftime("%Y-%m-%d"),
        "merch_lat": features["Lat (Merchant)"],
        "merch_long": features["Long (Merchant)"],
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Expecting: {"fraud_probability": float, "fraud": bool}
        fraud_prob = data.get("fraud_probability", None)
        st.markdown("---")
        st.markdown("### :abakus: Prediction Result")
        if fraud_prob is None:
            st.warning("The API response did not contain `fraud_probability` :nachdenkliches_gesicht:")
            st.json(data)
        else:
            prob_percent = round(fraud_prob * 100, 2)

            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric(
                    label="Fraud probability",
                    value=f"{prob_percent} %"
                )
            with col2:
                if fraud_prob > 0.5:
                    st.error(":rundumleuchte: **High risk: This transaction is likely FRAUDULENT.**")
                else:
                    st.success(":weißes_häkchen: **Low risk: This transaction is likely NOT fraud.**")
            with st.expander(":lupe_rechts: Raw API response"):
                st.json(data)
    except requests.exceptions.RequestException as e:
        st.error(f"Error while calling the prediction API: {e}")
