import streamlit as st
import requests

st.markdown('''
# Challenge 1 : Streamlit for restitution
''')
Amount = st.number_input("Amount", format="%.6f")
V1 = st.number_input("V1", format="%.6f")
V2 = st.number_input("V2", format="%.6f")
V3 = st.number_input("V3", format="%.6f")
V4 = st.number_input("V4", format="%.6f")
V5 = st.number_input("V5", format="%.6f")
V6 = st.number_input("V6", format="%.6f")
V7 = st.number_input("V7", format="%.6f")
V8 = st.number_input("V8", format="%.6f")
V9 = st.number_input("V9", format="%.6f")
V10 = st.number_input("V10", format="%.6f")
V11 = st.number_input("V11", format="%.6f")
V12 = st.number_input("V12", format="%.6f")
V13 = st.number_input("V13", format="%.6f")
V14 = st.number_input("V14", format="%.6f")
V15 = st.number_input("V15", format="%.6f")
V16 = st.number_input("V16", format="%.6f")
V17 = st.number_input("V17", format="%.6f")
V18 = st.number_input("V18", format="%.6f")
V19 = st.number_input("V19", format="%.6f")
V20 = st.number_input("V20", format="%.6f")
V21 = st.number_input("V21", format="%.6f")
V22 = st.number_input("V22", format="%.6f")
V23 = st.number_input("V23", format="%.6f")
V24 = st.number_input("V24", format="%.6f")
V25 = st.number_input("V25", format="%.6f")
V26 = st.number_input("V26", format="%.6f")
V27 = st.number_input("V27", format="%.6f")
V28 = st.number_input("V28", format="%.6f")

# url = "https://taxifare.lewagon.ai/predict"
url = "http://127.0.0.1:8000/predict"
params = {
    "Time": "2025-01-01 19:18:00",
    "Amount": Amount,
    "V1": V1,
    "V2": V2,
    "V3": V3,
    "V4": V4,
    "V5": V5,
    "V6": V6,
    "V7": V7,
    "V8": V8,
    "V9": V9,
    "V10": V10,
    "V11": V11,
    "V12": V12,
    "V13": V13,
    "V14": V14,
    "V15": V15,
    "V16": V16,
    "V17": V17,
    "V18": V18,
    "V19": V19,
    "V20": V20,
    "V21": V21,
    "V22": V22,
    "V23": V23,
    "V24": V24,
    "V25": V25,
    "V26": V26,
    "V27": V27,
    "V28": V28
}

response = requests.get(url, params=params)

print(response.json())

# Display the result in Streamlit
st.write("### Predicted :")
st.json(response.json())
