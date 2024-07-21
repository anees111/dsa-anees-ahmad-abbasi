import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Optional, List, Tuple, Union
import pickle
import logging
from __init__ import FEATURES_TO_SCALE, SCALER_PATH,DROPPED_COLUMNS_001, RENAMING_DICT

logging.basicConfig(level=logging.DEBUG)

def load_scaler(scaler_path: str) -> StandardScaler:
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    return scaler

def preprocess_test_data(test_data: pd.DataFrame, scaler_path: str, window_size: int) -> np.ndarray:
    # Ensure the dataframe has the correct headers
    test_data.columns = list(RENAMING_DICT.values())
    
    # Load the scaler
    scaler = load_scaler(scaler_path)
    
    # Drop unnecessary columns
    columns_to_drop = [col for col in DROPPED_COLUMNS_001 + ["cycle_num"] if col in test_data.columns]
    test_data.drop(columns=columns_to_drop, inplace=True)
    
    # Scale features
    scaled_features = scaler.transform(test_data[FEATURES_TO_SCALE])
    scaled_test_df = pd.DataFrame(scaled_features, columns=FEATURES_TO_SCALE)
    scaled_test_df['engine_num'] = test_data['engine_num'].values
    logging.debug(f"Scaled test DataFrame head: \n{scaled_test_df.head()}")  # Debugging info

    if scaled_test_df['engine_num'].nunique() == 1:
        X_test = preprocess_single_engine(scaled_test_df, window_size)
    else:
        X_test = preprocess_multiple_engines(scaled_test_df, 'engine_num', ['engine_num'], window_size)
    
    return X_test

def preprocess_single_engine(data: pd.DataFrame, window_size: int) -> np.ndarray:
    data = data[FEATURES_TO_SCALE]  # Ensure only the required features are included
    if len(data) < window_size:
        raise ValueError(f"Window size {window_size} is greater than the number of rows in the data.")
    elif len(data) == window_size:
        last_window_data = data.values
    else:
        last_window_data = data.iloc[-window_size:].values

    logging.debug(f"Preprocessed single engine data: {last_window_data}")  # Debugging info
    return np.array([last_window_data])

def preprocess_multiple_engines(data: pd.DataFrame, feature_to_split: Union[str, int], feature_to_drop: List[str], window_size: int) -> np.ndarray:
    unique_splits = data[feature_to_split].unique()
    processed_data = []
    
    for split_value in unique_splits:
        data_temp = data[data[feature_to_split] == split_value].drop(columns=feature_to_drop, errors='ignore')
        data_temp = data_temp[FEATURES_TO_SCALE]  # Ensure only the required features are included
        
        if len(data_temp) < window_size:
            raise ValueError(f"Window size {window_size} is greater than the number of rows in the data for engine {split_value}.")
        
        last_window_data = data_temp.iloc[-window_size:].values
        processed_data.append(last_window_data)
    
    logging.debug(f"Preprocessed multiple engines data: {processed_data}")  # Debugging info
    return np.array(processed_data)
