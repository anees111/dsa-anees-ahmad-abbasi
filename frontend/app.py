import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
 
import streamlit as st
import requests
import pandas as pd
from model import ModelManager  # Import after adjusting the path
 
# FastAPI URL
API_URL = "http://127.0.0.1:8000/predict/"
 
st.title("Anomaly Detection")
 
# Upload CSV file
uploaded_file = st.file_uploader("Upload your data CSV file with 24 features", type=["csv"])
 
if uploaded_file:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
 
    # Check if the data has the expected number of features (24)
    if df.shape[1] != 24:
        st.error(f"Expected 24 features, but got {df.shape[1]}.")
        st.error("Please upload a CSV file with exactly 24 features.")
    else:
        # Convert DataFrame to list for prediction
        data = df.values.tolist()
        # st.write("Data for Prediction:", data)  # Debug print
 
        # Prepare data for API request
        response = requests.post(API_URL, json={"data": data})
 
        if response.status_code == 200:
            result = response.json()
            predictions = result["predictions"]
 
            # Ensure predictions is a list of numbers
            if isinstance(predictions, list):
                st.write("Predictions:", predictions)
                
                # Compute anomalies
                anomalies = [1 if pred < 0 else 0 for pred in predictions]
                st.write("Anomalies:", anomalies)
            else:
                st.error("Unexpected format of predictions.")
        else:
            st.error(f"Error {response.status_code}: {response.text}")