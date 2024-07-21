import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCALER_PATH = os.path.join(BASE_DIR, '../items/scaler_001.pkl')
MODEL_PATH_LIST = [
    os.path.join(BASE_DIR, '../items/final_model.h5'),
    os.path.join(BASE_DIR, '../items/window_1_model.h5'),
    os.path.join(BASE_DIR, '../items/window_5_model.h5'),
    os.path.join(BASE_DIR, '../items/window_10_model.h5'),
    os.path.join(BASE_DIR, '../items/window_15_model.h5')
]
WINDOW_SIZE_LIST = [30, 1, 5, 10, 15]

# Features
DROPPED_COLUMNS_001 = [
    'oper_set_3', 'temp_fan_inlet', 'engine_px_ratio', 'demanded_fan_speed',
    'demanded_corr_fan_speed', 'px_fan_inlet', 'px_by_duct', 'fuel_air_ratio', 'corr_core_speed'
]

RENAMING_DICT = {
    0: "engine_num", 1: "cycle_num", 2: "oper_set_1", 3: "oper_set_2", 4: "oper_set_3", 5: "temp_fan_inlet",
    6: "temp_lpc_outlet", 7: "temp_hpc_outlet", 8: "temp_lpt_outlet", 9: "px_fan_inlet", 10: "px_by_duct",
    11: "px_hpc_outlet", 12: "phys_fan_speed", 13: "phys_core_speed", 14: "engine_px_ratio",
    15: "stat_px_hpc_out", 16: "fuel_flow_ratio", 17: "corr_fan_speed", 18: "corr_core_speed",
    19: "bypass_ratio", 20: "fuel_air_ratio", 21: "bleed_enthalpy", 22: "demanded_fan_speed",
    23: "demanded_corr_fan_speed", 24: "hpt_coolant_bleed", 25: "lpt_coolant_bleed"
}

FEATURES_TO_SCALE = [
    'oper_set_1', 'oper_set_2', 'temp_lpc_outlet', 'temp_hpc_outlet', 'temp_lpt_outlet',
    'px_hpc_outlet', 'phys_fan_speed', 'phys_core_speed', 'stat_px_hpc_out',
    'fuel_flow_ratio', 'corr_fan_speed', 'bypass_ratio', 'bleed_enthalpy',
    'hpt_coolant_bleed', 'lpt_coolant_bleed'
]
