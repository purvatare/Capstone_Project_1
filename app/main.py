from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

# Load model and scaler
model = joblib.load("/Users/purvatare/Documents/manufacturing-output-prediction/models/linear_regression_model.pkl")
scaler = joblib.load("/Users/purvatare/Documents/manufacturing-output-prediction/models/scaler.pkl")


@app.get("/")
def home():
    return {"message": "Manufacturing Prediction API is running"}


@app.post("/predict")
def predict(data: dict):
    try:
        # Convert input to numpy array
        features = np.array(list(data.values())).reshape(1, -1)

        # Scale input
        scaled_features = scaler.transform(features)

        # Predict
        prediction = model.predict(scaled_features)

        return {"prediction": float(prediction[0])}

    except Exception as e:
        return {"error": str(e)}
