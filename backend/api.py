# backend/api.py

from fastapi import FastAPI, File, UploadFile, Depends
import pandas as pd
import joblib
import h5py
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from io import BytesIO
from sqlalchemy.orm import Session
from models import ProcessedData, SessionLocal

app = FastAPI()

# Load the Isolation Forest model from the HDF5 file
def load_model():
    with h5py.File(r'D:\AL-\action_learning\items\isolation_forest_model.h5', 'r') as hf:
        model_data = hf['model'][:]
    model = joblib.load(BytesIO(model_data))
    return model

model = load_model()
scaler = StandardScaler()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/detect_anomalies/")
async def detect_anomalies(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    df = pd.read_csv(BytesIO(contents), header=None)
    
    if df.empty:
        return {"error": "Uploaded file is empty or invalid."}
    
    # Standardize the data
    data_scaled = scaler.fit_transform(df)
    
    # Predict anomalies
    predictions = model.predict(data_scaled)
    df['anomaly'] = predictions
    
    # Store processed data into the database
    for index, row in df.iterrows():
        db_data = ProcessedData(
            feature_1=row[0],  # Adjust according to the actual feature names
            feature_2=row[1],  # Adjust according to the actual feature names
            anomaly=int(row['anomaly'])  # Ensure anomaly is converted to int
        )
        db.add(db_data)
    
    db.commit()  # Commit all changes to the database
    
    # Convert DataFrame to JSON for response
    result = df.to_json(orient='split')
    
    return {"data": result}
