from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import pandas as pd
import numpy as np
import pickle
import logging
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import custom_object_scope
from typing import List, Optional

# Import your preprocessing functions
from preprocess import preprocess_test_data

# Define your custom loss function
def asymmetric_loss(RUL_true, RUL_predicted, a1=10, a2=13):
    diff = tf.subtract(RUL_true, RUL_predicted)
    loss = tf.reduce_sum(tf.where(diff < 0, tf.exp(-diff/a1)-1, tf.exp(diff/a2)-1), axis=0)
    return loss

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Load models
model_paths = {
    1: "../items/window_1_model.h5",
    5: "../items/window_5_model.h5",
    10: "../items/window_10_model.h5",
    15: "../items/window_15_model.h5",
    30: "../items/final_model.h5",
}

models = {}

def load_custom_model(model_path):
    with custom_object_scope({'asymmetric_loss': asymmetric_loss}):
        try:
            model = load_model(model_path, custom_objects={'asymmetric_loss': asymmetric_loss})
        except ValueError as e:
            logging.error(f"Error loading model {model_path}: {e}")
            model = None
        return model

for window_size, model_path in model_paths.items():
    models[window_size] = load_custom_model(model_path)

class ModelInput(BaseModel):
    window_size: int
    data: Optional[List[float]] = None

@app.post("/predict/")
async def predict(input: ModelInput = None, file: UploadFile = File(None)):
    if file:
        data = pd.read_csv(file.file)
    else:
        if input and input.data:
            data = pd.DataFrame([input.data], columns=preprocess.RENAMING_DICT.values())
        else:
            return {"error": "No data provided"}
    
    try:
        window_size = input.window_size if input else None
        model = model_paths.get(window_size)
        if not model:
            return {"error": "Model not found for the given window size"}
        
        # Preprocess the data
        preprocessed_data = preprocess_test_data(data, preprocess.SCALER_PATH, window_size)
        
        # Predict using the model
        predictions = model.predict(preprocessed_data)
        
        return {"predictions": predictions.tolist()}
    
    except Exception as e:
        logging.error(f"Error during prediction: {str(e)}")
        return {"error": str(e)}
