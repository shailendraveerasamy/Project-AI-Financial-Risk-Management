import streamlit as st
import requests

st.markdown('''
# Challenge 1 : Streamlit for restitution
''')

pickup_longitude = st.number_input("Pickup longitude", format="%.6f")
pickup_latitude = st.number_input("Pickup latitude", format="%.6f")
dropoff_longitude = st.number_input("Dropoff longitude", format="%.6f")
dropoff_latitude = st.number_input("Dropoff latitude", format="%.6f")
passenger_count = st.number_input("Passenger count", min_value=1, max_value=8, step=1, format="%d")

url = "https://taxifare.lewagon.ai/predict"
params = {
    "pickup_datetime": "2014-07-06 19:18:00",
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude ,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}

response = requests.get(url, params=params)

print(response.json())

# Display the result in Streamlit
st.write("### Predicted Fare:")
st.json(response.json())
