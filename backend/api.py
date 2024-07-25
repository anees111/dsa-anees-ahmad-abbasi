from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import numpy as np
from model import ModelManager
from database import get_db
import logging
 
app = FastAPI()
model_manager = ModelManager('../items/isolation_forest_AD_model.h5')
 
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
 
class PredictionRequest(BaseModel):
    data: list
 
@app.on_event("startup")
def startup_event():
    model_manager.load_model()
    logger.info("Model loaded at startup.")
 
@app.post("/predict/")
def predict(request: PredictionRequest, db: Session = Depends(get_db)):
    try:
        data = np.array(request.data)
 
        # Ensure the data is not empty
        if data.size == 0:
            raise HTTPException(status_code=400, detail="Input data is empty.")
 
        # Ensure the data shape is correct
        if len(data.shape) == 1:
            data = data.reshape(1, -1)
        elif data.shape[1] != 24:
            if data.shape[1] > 24:
                data = data[:, :24]
            else:
                raise HTTPException(status_code=400, detail=f"Expected input shape (None, 24), but got {data.shape}")
 
        logger.debug("Data shape for prediction: %s", data.shape)
        predictions = model_manager.predict(data)
 
        # Flatten predictions if necessary and ensure it's a list
        if isinstance(predictions, np.ndarray):
            predictions = predictions.flatten().tolist()
        elif isinstance(predictions, list):
            # If predictions are already a list, ensure they are correctly formatted
            predictions = [item for sublist in predictions for item in sublist] if any(isinstance(i, list) for i in predictions) else predictions
        else:
            raise HTTPException(status_code=500, detail="Unexpected prediction format.")
 
        logger.debug("Predictions: %s", predictions)
        return {"predictions": predictions}
    except Exception as e:
        logger.error("Prediction error: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Prediction error.")