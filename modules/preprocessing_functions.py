# preprocessing_functions.py

import numpy as np
import pandas as pd
from typing import Tuple, List, Optional, Union

def preprocessing_for_lstm(data: pd.DataFrame, id_column: str, target: pd.Series, window_size: int = 30, columns_to_drop: Optional[List[str]] = None, max_rul: Optional[int] = None, shift: int = 1) -> Tuple[np.ndarray, np.ndarray]:
    if columns_to_drop is None:
        columns_to_drop = []
        
    assert id_column in data.columns, "id_column not in data columns"
    assert isinstance(columns_to_drop, list), "columns_to_drop must be a list"
    
    engines_nums = data[id_column].unique()
    num_features = data.shape[1] - len(columns_to_drop)
    
    features_3d = []
    targets_1d = []
    
    for engine_num in engines_nums:
        engine_data = data[data[id_column] == engine_num].drop(columns=columns_to_drop)
        engine_target = target[data[id_column] == engine_num]
        
        if len(engine_data) <= window_size:
            raise ValueError(f"Window size greater than data at unit number: {engine_num}")
        
        for start in range(0, len(engine_data) - window_size + 1, shift):
            end = start + window_size
            features_3d.append(engine_data.iloc[start:end].values)
            targets_1d.append(engine_target.iloc[end - 1])
    
    features_3d = np.array(features_3d)
    targets_1d = np.array(targets_1d)
    
    if max_rul is not None:
        targets_1d = np.clip(targets_1d, None, max_rul)
    
    return features_3d, targets_1d

def preprocessing_test(data: pd.DataFrame, feature_to_split: Union[str, int], feature_to_drop: List[str], window_size: int = 30) -> np.ndarray:
    assert isinstance(feature_to_drop, list), "feature_to_drop must be a list"
    
    unique_splits = data[feature_to_split].unique()
    num_features = data.shape[1] - len(feature_to_drop)
    
    processed_data = []
    
    for split_value in unique_splits:
        data_temp = data[data[feature_to_split] == split_value].drop(columns=feature_to_drop)
        
        if len(data_temp) < window_size:
            raise ValueError(f"Window size greater than data length for split value: {split_value}")
        
        last_window_data = data_temp.iloc[-window_size:].values
        processed_data.append(last_window_data)
    
    processed_data = np.array(processed_data)
    
    return processed_data
