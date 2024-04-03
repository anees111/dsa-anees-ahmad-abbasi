import streamlit as st
import pandas as pd
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import psycopg2

# Initialize FastAPI
app = FastAPI()

# PostgreSQL connection details
DB_HOST = 'localhost'
DB_NAME = 'dsp_project'
DB_USER = 'postgres'
DB_PASSWORD = 'pass123'

# Define a model for prediction request
class PredictionRequest(BaseModel):
    feature1: str
    feature2: str
    feature3: str
    feature4: str
    feature5: float
    feature6: str

# Define a model for prediction response
class PredictionResponse(BaseModel):
    prediction: float

# Define a model for past predictions response
class PastPredictionsResponse(BaseModel):
    predictions: List[float]
    features: List[Dict[str, str]]

# Function to make predictions using API
def make_predictions(features):
    # Example code to make API call, replace it with your actual API call
    api_url = "http://localhost:5000/predict"
    response = requests.post(api_url, json=features)
    predictions = response.json()
    return predictions

# Function to connect to PostgreSQL database
def connect_to_db():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn

# Function to save prediction and features to the database
def save_to_db(prediction, features):
    conn = connect_to_db()
    cursor = conn.cursor()
    insert_query = "INSERT INTO past_predictions (prediction, feature1, feature2, feature3, feature4, feature5, feature6) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (prediction, features['feature1'], features['feature2'], features['feature3'], features['feature4'], features['feature5'], features['feature6']))
    conn.commit()
    cursor.close()
    conn.close()

# FastAPI endpoint for making predictions
@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    features = request.dict()
    prediction = make_predictions(features)
    # Save prediction to the database
    save_to_db(prediction['prediction'], features)
    return {"prediction": prediction['prediction']}

# FastAPI endpoint for retrieving past predictions
@app.get("/past-predictions", response_model=PastPredictionsResponse)
def past_predictions(start_date: str, end_date: str, prediction_source: str):
    # Connect to the database
    conn = connect_to_db()
    cursor = conn.cursor()
    # Query past predictions based on selected criteria
    select_query = "SELECT prediction, feature1, feature2, feature3, feature4, feature5, feature6 FROM past_predictions WHERE date BETWEEN %s AND %s"
    cursor.execute(select_query, (start_date, end_date))
    past_predictions_data = cursor.fetchall()
    cursor.close()
    conn.close()
    # Process past predictions data
    predictions = [row[0] for row in past_predictions_data]
    features = [{'feature1': row[1], 'feature2': row[2], 'feature3': row[3], 'feature4': row[4], 'feature5': row[5], 'feature6': row[6]} for row in past_predictions_data]
    return {"predictions": predictions, "features": features}

# Prediction webpage
def prediction_page():
    st.title("Flight Price Prediction")
    st.subheader("Prediction Page")
    
    # Form for single sample prediction
    st.subheader("Single Sample Prediction")
    # Define input fields for features
    feature1 = st.text_input("Airline", value="")
    feature2 = st.text_input("Flight", value="")
    feature3 = st.text_input("Source City", value="")
    feature4 = st.text_input("Departure Time", value="")
    feature5 = st.number_input("Stops", value=0.0)
    feature6 = st.text_input("Arrival Time", value="")
    
    # Predict button
    if st.button("Predict"):
        features = {
            "feature1": feature1,
            "feature2": feature2,
            "feature3": feature3,
            "feature4": feature4,
            "feature5": feature5,
            "feature6": feature6
        }
        prediction = make_predictions(features)
        # Save prediction to the database
        save_to_db(prediction['prediction'], features)
        st.write("Prediction:", prediction['prediction'])
        st.write("Features:", features)

# Past predictions webpage
def past_predictions_page():
    st.title("Flight Price Prediction")
    st.subheader("Past Predictions Page")
    # Date selection component
    start_date = st.text_input("Start Date")
    end_date = st.text_input("End Date")
    # Prediction source drop list
    prediction_source = st.selectbox("Prediction Source", ["webapp", "scheduled predictions", "all"])

    # Call FastAPI endpoint to retrieve past predictions
    response = requests.get("/past-predictions", params={"start_date": start_date, "end_date": end_date, "prediction_source": prediction_source})
    if response.status_code == 200:
        past_predictions_data = response.json()
        st.write("Past Predictions:", past_predictions_data["predictions"])
        st.write("Features:", past_predictions_data["features"])
    else:
        st.write("Failed to retrieve past predictions")

# Main function to run the web app
def main():
    page = st.sidebar.selectbox("Select Page", ["Prediction Page", "Past Predictions Page"])
    
    if page == "Prediction Page":
        prediction_page()
    elif page == "Past Predictions Page":
        past_predictions_page()

if __name__ == "__main__":
    main()
