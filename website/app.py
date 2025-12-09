import streamlit as st
import requests

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
    based on its amount, timestamp, and anonymized PCA features *(V1–V28)*.
    """
)

st.markdown("---")

# --------------------------
# Input form
# --------------------------
# Backend URL
# url = "https://taxifare.lewagon.ai/predict"
url = "http://127.0.0.1:8001/predict"

with st.form("fraud_form"):
    # Time + Amount at the top
    top_col1, top_col2 = st.columns([2, 1])

    with top_col1:
        Time = st.text_input("🕒 Time (YYYY-MM-DD HH:MM:SS)", value="2013-01-01 12:00:00")

    with top_col2:
        Amount = st.number_input("💰 Amount", format="%.6f", min_value=0.0, value=100.0)

    st.markdown("### 🔢 Anonymized Transaction Features (V1 – V28)")

    # Feature grid
    feature_names = [f"V{i}" for i in range(1, 29)]
    features = {}

    cols = st.columns(4)  # 4 columns grid

    for idx, feature in enumerate(feature_names):
        col = cols[idx % 4]
        with col:
            features[feature] = st.number_input(
                feature,
                format="%.6f",
                value=0.0,
                key=feature
            )

    # Submit button
    st.markdown(" ")
    submit = st.form_submit_button("🔍 Predict Fraud Score")

# --------------------------
# Prediction logic
# --------------------------
if submit:
    # Prepare params for API
    params = {
        "Time": Time,
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
