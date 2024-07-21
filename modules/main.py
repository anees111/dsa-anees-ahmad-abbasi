from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import custom_object_scope
import os
import logging
import io
from preprocess import preprocess_test_data

app = FastAPI()

# Allow CORS for all origins (adjust as necessary for your use case)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define your custom loss function
def asymmetric_loss(RUL_true, RUL_predicted, a1=10, a2=13):
    diff = tf.subtract(RUL_true, RUL_predicted)
    loss = tf.reduce_sum(tf.where(diff < 0, tf.exp(-diff/a1)-1, tf.exp(diff/a2)-1), axis=0)
    return loss

# Path to the models directory
MODEL_DIR = "../items"

# Variables to hold the loaded models
model_1 = None
model_5 = None
model_10 = None
model_15 = None
model_30 = None

# Function to load a model
def load_custom_model(model_path):
    with custom_object_scope({'asymmetric_loss': asymmetric_loss}):
        try:
            model = load_model(model_path, custom_objects={'asymmetric_loss': asymmetric_loss})
            logging.info(f"Loaded model from {model_path}")
            return model
        except Exception as e:
            logging.error(f"Error loading model {model_path}: {e}")
            return None

# Load all models at startup
@app.on_event("startup")
async def load_models():
    global model_1, model_5, model_10, model_15, model_30
    
    model_1 = load_custom_model(os.path.join(MODEL_DIR, "window_1_model.h5"))
    model_5 = load_custom_model(os.path.join(MODEL_DIR, "window_5_model.h5"))
    model_10 = load_custom_model(os.path.join(MODEL_DIR, "window_10_model.h5"))
    model_15 = load_custom_model(os.path.join(MODEL_DIR, "window_15_model.h5"))
    model_30 = load_custom_model(os.path.join(MODEL_DIR, "final_model.h5"))

# Endpoint to upload and display CSV file contents
@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')), header=None)
    return {"filename": file.filename, "data": df.to_dict()}  # Returning the entire data for demonstration

# Endpoint to preprocess CSV file based on window size
@app.post("/preprocess/")
async def preprocess_file(file: UploadFile = File(...), window_size: int = Form(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')), header=None)
    
    try:
        preprocessed_data = preprocess_test_data(df, "../items/scaler_001.pkl", window_size)
        return {"data_shape": preprocessed_data.shape, "data": preprocessed_data.tolist()}
    except Exception as e:
        logging.error(f"Error during preprocessing: {str(e)}")
        return {"error": str(e)}

# Test endpoint to verify models are loaded
@app.get("/models")
async def get_loaded_models():
    loaded_models = {
        "model_1": "loaded" if model_1 else "not loaded",
        "model_5": "loaded" if model_5 else "not loaded",
        "model_10": "loaded" if model_10 else "not loaded",
        "model_15": "loaded" if model_15 else "not loaded",
        "model_30": "loaded" if model_30 else "not loaded"
    }
    return loaded_models

# Run the app with `uvicorn main:app --reload`
