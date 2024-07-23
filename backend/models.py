# backend/models.py

from sqlalchemy import Column, Integer, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Update the DATABASE_URL to use SQLite
DATABASE_URL = "sqlite:///./test.db"

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the ProcessedData model
class ProcessedData(Base):
    __tablename__ = "processed_data"

    id = Column(Integer, primary_key=True, index=True)
    feature_1 = Column(Float)
    feature_2 = Column(Float)
    anomaly = Column(Integer)

# Create the tables in the database
Base.metadata.create_all(bind=engine)
