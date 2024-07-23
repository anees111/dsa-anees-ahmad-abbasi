# frontend/app.py

import streamlit as st
import requests
import pandas as pd

st.title("Anomaly Detection and Data Storage")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Send the file to the FastAPI server
    response = requests.post("http://127.0.0.1:8000/detect_anomalies/", files={"file": uploaded_file.getvalue()})

    if response.status_code == 200:
        data = response.json()
        st.write("Processed Data:")
        st.write(pd.read_json(data["data"], orient='split'))
    else:
        st.write("Failed to get response from server")
