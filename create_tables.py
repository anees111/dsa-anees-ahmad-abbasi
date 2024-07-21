# create_tables.py

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, TIMESTAMP
from datetime import datetime

DATABASE_URL = "postgresql://rul_user:12345678@localhost/rul_db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define the input_data table
input_data_table = Table(
    "input_data",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("engine_num", Integer),
    Column("oper_set_1", Float),
    Column("oper_set_2", Float),
    Column("temp_lpc_outlet", Float),
    Column("temp_hpc_outlet", Float),
    Column("temp_lpt_outlet", Float),
    Column("px_hpc_outlet", Float),
    Column("phys_fan_speed", Float),
    Column("phys_core_speed", Float),
    Column("stat_px_hpc_out", Float),
    Column("fuel_flow_ratio", Float),
    Column("corr_fan_speed", Float),
    Column("bypass_ratio", Float),
    Column("bleed_enthalpy", Float),
    Column("hpt_coolant_bleed", Float),
    Column("lpt_coolant_bleed", Float),
    Column("timestamp", TIMESTAMP, default=datetime.utcnow),
)

# Define the predictions table
predictions_table = Table(
    "predictions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("input_data_id", Integer, sqlalchemy.ForeignKey("input_data.id")),
    Column("predicted_rul", Float),
    Column("window_size", Integer),
    Column("model_used", String),
    Column("timestamp", TIMESTAMP, default=datetime.utcnow),
)

metadata.create_all(engine)

print("Tables created successfully.")
