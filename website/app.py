import streamlit as st
import requests
from datetime import datetime

# --------------------------
# Page config
# --------------------------
st.set_page_config(
    page_title="Fraud Detection Demo",
    page_icon="💳",
    layout="wide"
)

# --------------------------
# Basic styling (CSS)
# --------------------------
st.markdown("""
<style>
/* ✅ Light, clean background */
.stApp {
    background: radial-gradient(circle at top left, #ffffff 0%, #f8fafc 40%, #e5e7eb 100%);
}

/* ✅ White content card */
.block-container {
    background: #ffffff;
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

/* ✅ Title styling */
h1, h2, h3 {
    font-weight: 700;
    color: #111827;
}

/* ✅ Normal text */
p, label, span {
    color: #374151;
}

/* ✅ Sleeker number + text inputs */
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    border-radius: 10px;
    background-color: #f9fafb;
}

/* ✅ Full-width primary button */
div[data-testid="baseButton-secondary"],
div[data-testid="baseButton-primary"] {
    width: 100%;
    border-radius: 12px;
}

/* Fix text colour inside st.text_input */
.stTextInput input {
    color: #111827 !important;         /* dark text */
    background-color: #f9fafb !important;
}

/* Fix placeholder colour */
.stTextInput input::placeholder {
    color: #6b7280 !important;         /* subtle gray */
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
    st.subheader("💳 About this demo")
    st.write(
        "This app sends transaction features to a fraud detection model "
        "and returns the **likelihood of credit card fraud**."
    )
    st.markdown("---")
    st.caption("Enter the features on the right and click **Predict Fraud Score**.")

# --------------------------
# Header
# --------------------------
st.markdown("## 💳 Fraud Detection Demo")
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
# url = "https://taxifare.lewagon.ai/predict"
url = "https://fraud-app-546443544540.europe-west1.run.app"

# --------------------------
# Input form
# --------------------------
with st.form("fraud_form"):

    # Amount only (Time removed completely)
    Amount = st.number_input("💰 Amount", format="%.6f", min_value=0.0, value=10000.0)

    st.markdown("### 🔢 Transaction Features")

    feature_config = {
        "Transaction date/ time": {"type": "datetime"},
        "Category": {"type": "select", "options": ["Food", "Travel", "Shopping", "Other"]},
        "Gender": {"type": "select", "options": ["Male", "Female", "Other"]},
        "Lat (Cardholder)": {"type": "number"},
        "Long (Cardholder)": {"type": "number"},
        "Date of Birth": {"type": "date"},
        "Lat (Merchant)": {"type": "number"},
        "Long (Merchant)": {"type": "number"},
    }

    features = {}
    cols = st.columns(4)  # 4-column grid

    for idx, (feature, config) in enumerate(feature_config.items()):
        col = cols[idx % 4]
        with col:
            if config["type"] == "number":
                features[feature] = st.number_input(
                    feature,
                    format="%.6f",
                    value=0.0,
                    key=feature,
                )
            elif config["type"] == "select":
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

    # Submit button
    st.markdown(" ")
    submit = st.form_submit_button("🔍 Predict Fraud Score")

# --------------------------
# Prediction logic
# --------------------------
if submit:
    # Prepare params for API (no Time here anymore)
    params = {
        "Amount": Amount,
        **features,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        fraud_prob = data.get("fraud_probability", None)

        st.markdown("---")
        st.markdown("### 🧮 Prediction Result")

        if fraud_prob is None:
            st.warning("The API response did not contain `fraud_probability` 🤔")
            st.json(data)
        else:
            prob_percent = round(fraud_prob * 100, 2)

            # Nice metric display
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric(
                    label="Fraud probability",
                    value=f"{prob_percent} %"
                )

            with col2:
                if fraud_prob > 0.5:
                    st.error("🚨 **High risk: This transaction is likely FRAUDULENT.**")
                else:
                    st.success("✅ **Low risk: This transaction is likely NOT fraud.**")

            with st.expander("🔎 Raw API response"):
                st.json(data)

    except requests.exceptions.RequestException as e:
        st.error(f"Error while calling the prediction API: {e}")
