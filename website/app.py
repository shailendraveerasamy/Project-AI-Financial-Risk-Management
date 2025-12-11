import streamlit as st
import requests
from datetime import datetime, date

# --------------------------
# Page config
# --------------------------
st.set_page_config(
    page_title="Fraud Detection",
    page_icon="💳",
    layout="wide"
)

# --------------------------
# Basic styling (CSS)
# --------------------------
st.markdown(
    """
<style>
/* Light, clean background */
.stApp {
    background: radial-gradient(circle at top left, #FFFFFF 0%, #F8FAFC 40%, #E5E7EB 100%);
}

/* White content card */
.block-container {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

/* Title styling */
h1, h2, h3 {
    font-weight: 700;
    color: #111827;
}

/* Normal text */
p, label, span {
    color: #374151;
}

/* Sleeker number + text inputs */
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    border-radius: 10px;
    background-color: #F9FAFB;
}

/* Full-width primary button */
div[data-testid="baseButton-secondary"],
div[data-testid="baseButton-primary"] {
    width: 100%;
    border-radius: 12px;
}

/* Fix text colour inside st.text_input */
.stTextInput input {
    color: #111827 !important;
    background-color: #F9FAFB !important;
}

/* Fix placeholder colour */
.stTextInput input::placeholder {
    color: #6B7280 !important;
}

/* Force headings to be dark */
h1, h2, h3, h4, h5, h6,
.block-container h1,
.block-container h2,
.block-container h3,
.block-container h4,
.block-container h5,
.block-container h6 {
    color: #111827 !important;
}

/* Streamlit sometimes renders markdown headers as <p> tags */
.block-container p strong,
.block-container p em,
.block-container p {
    color: #111827 !important;
}
</style>
""",
    unsafe_allow_html=True
)

# --------------------------
# Sidebar
# --------------------------
with st.sidebar:
    st.subheader("💳 About this tool")
    st.write(
        "This app sends transaction features to a fraud detection model "
        "and returns the **likelihood of credit card fraud**."
    )
    st.markdown("---")
    st.caption("Enter the features on the right and click **Predict Fraud Score**.")

# --------------------------
# Header
# --------------------------
st.markdown("## 💳 Fraud Detection")
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
    "Canton, OH": {"lat": 40.8027, "long": -81.3739},
    "Delhi, LA": {"lat": 32.3929, "long": -91.4714},
    "Winger, MN": {"lat": 47.5375, "long": -95.9941},
    "Southfield, MI": {"lat": 42.4969, "long": -83.2911},
    "Thida, AR": {"lat": 35.5762, "long": -91.4539},
    "Chattanooga, TN": {"lat": 35.0271, "long": -85.2356},
    "Early, IA": {"lat": 42.4483, "long": -95.1726},
    "Walnut Ridge, AR": {"lat": 36.0244, "long": -90.9288},
    "Hawthorne, CA": {"lat": 33.9143, "long": -118.3493},
    "Haw River, NC": {"lat": 36.0424, "long": -79.3242},
    "Shrewsbury, MA": {"lat": 42.2848, "long": -71.7205},
    "Buellton, CA": {"lat": 34.6209, "long": -120.1922},
    "Falmouth, MI": {"lat": 44.2529, "long": -85.0170},
    "Newberg, OR": {"lat": 45.3099, "long": -122.9685},
    "Marion, CT": {"lat": 41.7918, "long": -72.7188},
    # New cardholder locations
    "Columbia, SC": {"lat": 33.9659, "long": -80.9355},
    "Talmage, UT": {"lat": 40.3207, "long": -110.436},
    "New Diggins, WI": {"lat": 42.5545, "long": -90.3508},
    "Florida Ridge, FL": {"lat": 27.6330, "long": -80.40318},
    "Odessa, TX": {"lat": 31.8599, "long": -102.7413},
}

MERCHANT_LOCATIONS = {
    "Southfield Mall, MI": {"lat": 42.4969, "long": -83.2911},
    "Hawthorne Retail, CA": {"lat": 33.9143, "long": -118.3493},
    "Chattanooga Outlet, TN": {"lat": 35.0271, "long": -85.2356},
    "Shrewsbury Plaza, MA": {"lat": 42.2848, "long": -71.7205},
    "Newberg Online Hub, OR": {"lat": 45.3099, "long": -122.9685},
    # New merchant locations
    "Lexington, SC": {"lat": 33.986391, "long": -81.200714},
    "Price, UT": {"lat": 39.450498, "long": -109.960431},
    "Darlington, WI": {"lat": 42.771834, "long": -90.158365},
    "Palm City, FL": {"lat": 27.059901, "long": -80.32383},
    "Fort Piece, FL": {"lat": 27.27806, "long": -79.597618},
    "Andrews, TX": {"lat": 32.5758, "long": -102.60429},
}

# --------------------------
# Mapping: UI label -> model category value
# --------------------------
CATEGORY_TO_MODEL = {
    "Miscellaneous (Online)": "misc_net",
    "Miscellaneous (In-Store)": "misc_pos",
    "Entertainment": "entertainment",
    "Gas & Transport": "gas_transport",
    "Groceries (In-Store)": "grocery_pos",
    "Grocery (Online)": "grocery_net",
    "Shopping (Online)": "shopping_net",
    "Shopping (In-Store)": "shopping_pos",
    "Food & Dining": "food_dining",
    "Personal Care": "personal_care",
    "Health & Fitness": "health_fitness",
    "Travel": "travel",
    "Kids & Pets": "kids_pets",
    "Home": "home",
}

# --------------------------
# Feature configuration (for the UI)
# --------------------------
feature_config = {
    "Transaction date/ time": {"type": "datetime"},
    "Category": {
        "type": "select",
        "options": [
            "Miscellaneous (Online)",   # misc_net
            "Miscellaneous (In-Store)", # misc_pos
            "Entertainment",            # entertainment
            "Gas & Transport",          # gas_transport
            "Groceries (In-Store)",     # grocery_pos
            "Grocery (Online)",         # grocery_net
            "Shopping (Online)",        # shopping_net
            "Shopping (In-Store)",      # shopping_pos
            "Food & Dining",            # food_dining
            "Personal Care",            # personal_care
            "Health & Fitness",         # health_fitness
            "Travel",                   # travel
            "Kids & Pets",              # kids_pets
            "Home",                     # home
        ],
    },
    "Gender": {"type": "select", "options": ["M", "F"]},
    "Date of Birth": {"type": "date"},
}

# --------------------------
# Input form
# --------------------------
with st.form("fraud_form"):
    # Transaction amount
    amt = st.number_input("💰 Amount", format="%.6f", min_value=0.0, value=10000.0)

    st.markdown("### 🔢 Transaction Features")

    features = {}
    cols = st.columns(4)  # 4-column grid

    for idx, (feature, config) in enumerate(feature_config.items()):
        col = cols[idx % 4]
        with col:
            if config["type"] == "select":
                features[feature] = st.selectbox(
                    feature,
                    config["options"],
                    key=feature,
                )
            elif config["type"] == "datetime":
                features[feature] = st.datetime_input(
                    feature,
                    value=datetime.now(),
                    key=feature,
                )
            elif config["type"] == "date":
                features[feature] = st.date_input(
                    feature,
                    value=date(1990, 1, 1),
                    min_value=date(1920, 1, 1),   # lower bound for DOB
                    max_value=date(2026, 1, 1),   # upper bound for DOB
                    key=feature,
                )

    st.markdown("### 📍 Locations")

    col_loc1, col_loc2 = st.columns(2)

    with col_loc1:
        cardholder_location = st.selectbox(
            "Cardholder location",
            list(CARDHOLDER_LOCATIONS.keys()),
            key="cardholder_location",
        )

    with col_loc2:
        merchant_location = st.selectbox(
            "Merchant location",
            list(MERCHANT_LOCATIONS.keys()),
            key="merchant_location",
        )

    # Optional: show what is actually sent to the model (geolocation)
    with st.expander("Advanced (optional): coordinates used for the model"):
        st.write("These values are sent to the model, but you don't need to edit them.")
        st.json(
            {
                "cardholder": CARDHOLDER_LOCATIONS[cardholder_location],
                "merchant": MERCHANT_LOCATIONS[merchant_location],
            }
        )

    # Submit button
    st.markdown(" ")
    submit = st.form_submit_button("🔍 Predict Fraud Score")

# --------------------------
# Prediction logic
# --------------------------
if submit:
    # Extract and format values for API
    trans_dt = features["Transaction date/ time"]
    dob = features["Date of Birth"]

    # Look up coordinates from the selected locations
    cardholder_coords = CARDHOLDER_LOCATIONS[cardholder_location]
    merchant_coords = MERCHANT_LOCATIONS[merchant_location]

    # Kategorie fürs Model umwandeln
    category_display = features["Category"]
    category_model_value = CATEGORY_TO_MODEL.get(category_display)

    if category_model_value is None:
        st.error(f"Unknown category selected: {category_display}")
    else:
        params = {
            "trans_date_trans_time": trans_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "category": category_model_value,  # Model-Name, nicht Label
            "amt": amt,
            "gender": features["Gender"],
            "lat": cardholder_coords["lat"],
            "long": cardholder_coords["long"],
            "dob": dob.strftime("%Y-%m-%d"),
            "merch_lat": merchant_coords["lat"],
            "merch_long": merchant_coords["long"],
        }

        # Optional: show all values sent to the model
        with st.expander("Advanced (optional): values sent to the model"):
            st.json(
                {
                    "category_display": category_display,
                    "category_model_value": category_model_value,
                    "params": params,
                }
            )

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Try several possible keys from the backend
            fraud_prob = data.get("fraud_probability", None)
            if fraud_prob is None:
                fraud_prob = data.get("The likelihood of being a Fraud is ", None)  # with space
            if fraud_prob is None:
                fraud_prob = data.get("The likelihood of being a Fraud is", None)   # without space

            # Optional: derive fraud flag (if present)
            fraud_flag = data.get("fraud", None)

            st.markdown("---")
            st.markdown("### 🧮 Prediction Result")

            if fraud_prob is None:
                st.warning("The API response did not contain a usable fraud probability 🤔")
                st.json(data)
            else:
                prob_percent = round(float(fraud_prob) * 100, 2)
                col1, col2 = st.columns([1, 2])

                with col1:
                    st.metric(
                        label="Fraud probability",
                        value=f"{prob_percent} %",
                    )

                with col2:
                    if fraud_flag is None:
                        fraud_flag = float(fraud_prob) > 0.5

                    if fraud_flag:
                        st.error("🚨 **High risk: This transaction is likely FRAUDULENT.**")
                    else:
                        st.success("✅ **Low risk: This transaction is likely NOT fraud.**")

                with st.expander("🔍 Raw API response"):
                    st.json(data)

        except requests.exceptions.RequestException as e:
            st.error(f"Error while calling the prediction API: {e}")
