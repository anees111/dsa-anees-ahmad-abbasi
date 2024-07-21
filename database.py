from sqlalchemy import create_engine, Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "postgresql://rul_user:12345678@localhost/rul_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class InputData(Base):
    __tablename__ = "input_data"

    id = Column(Integer, primary_key=True, index=True)
    engine_num = Column(Integer, nullable=False)
    oper_set_1 = Column(Float, nullable=False)
    oper_set_2 = Column(Float, nullable=False)
    temp_lpc_outlet = Column(Float, nullable=False)
    temp_hpc_outlet = Column(Float, nullable=False)
    temp_lpt_outlet = Column(Float, nullable=False)
    px_hpc_outlet = Column(Float, nullable=False)
    phys_fan_speed = Column(Float, nullable=False)
    phys_core_speed = Column(Float, nullable=False)
    stat_px_hpc_out = Column(Float, nullable=False)
    fuel_flow_ratio = Column(Float, nullable=False)
    corr_fan_speed = Column(Float, nullable=False)
    bypass_ratio = Column(Float, nullable=False)
    bleed_enthalpy = Column(Float, nullable=False)
    hpt_coolant_bleed = Column(Float, nullable=False)
    lpt_coolant_bleed = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    input_id = Column(Integer, ForeignKey("input_data.id"), nullable=False)
    prediction = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    input_data = relationship("InputData", back_populates="predictions")

InputData.predictions = relationship("Prediction", order_by=Prediction.id, back_populates="input_data")

Base.metadata.create_all(bind=engine)
