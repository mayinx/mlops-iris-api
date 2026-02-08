import os
import joblib
import numpy as np

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.joblib')

# Loading the trained model
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise RuntimeError(f"Model file not found at {MODEL_PATH}.")
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

app = FastAPI(
    title="Iris Prediction API",
    description="A simple API to predict Iris species based on sepal and petal measurements.",
    version="1.0.0",
)

# data model for input query
class IrisFeatures(BaseModel):
    petal_length: float
    petal_width: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "petal_length": 1.4,
                    "petal_width": 0.2,
                }
            ]
        }
    }

# prediction endpoint
@app.post("/predict")
def predict(features: IrisFeatures):
    try:
        input_features = np.array([
            features.petal_length,
            features.petal_width
        ]).reshape(1, -1)

        prediction = model.predict(input_features)
        prediction_proba = model.predict_proba(input_features)

        return {
            "prediction": int(prediction[0]),
            "prediction_proba": prediction_proba.tolist()[0]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
    
# health endpoint
# docker compose -p mlops exec nginx curl http://mlops-iris-api:8000/health
@app.get("/health")
def health():
    try:
        """Health endpoint to check if the API is operational."""
        return {"status": "ok"}    

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API Health error: {e}")
        
