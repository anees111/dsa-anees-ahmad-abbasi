import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
from tensorflow.keras.models import load_model as tf_load_model
from typing import Union, TextIO
from __init__ import SCALER_PATH, FEATURES_TO_SCALE,WINDOW_SIZE_LIST,MODEL_PATH_LIST
from preprocess import load_scaler, preprocess_test_data
from sklearn.preprocessing import StandardScaler

print(tf.__version__)