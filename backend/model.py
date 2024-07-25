import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np  # Ensure this import is present
import logging
 
 
class ModelManager:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
 
    def load_model(self):
        try:
            self.model = load_model(self.model_path)
            self.logger.info("Model loaded successfully.")
        except Exception as e:
            self.logger.error("Error loading model: %s", str(e))
        return self.model
 
    def predict(self, data):
        if self.model is None:
            self.logger.debug("Model is not loaded, loading model...")
            self.load_model()
 
        # Log the data shape
        self.logger.debug("Data shape for prediction: %s", data.shape)
 
        # Enable eager execution for debugging
        tf.config.run_functions_eagerly(True)
 
        try:
            predictions = self.model.predict(data)
            self.logger.debug("Predictions: %s", predictions)
 
            # Flatten predictions if necessary and ensure it's a list
            if isinstance(predictions, np.ndarray):
                predictions = predictions.flatten().tolist()
            elif isinstance(predictions, list):
                predictions = [item for sublist in predictions for item in sublist] if any(isinstance(i, list) for i in predictions) else predictions
            else:
                raise ValueError("Unexpected prediction format.")
 
            return predictions
        except Exception as e:
            self.logger.error("Error during prediction: %s", str(e), exc_info=True)
            raise