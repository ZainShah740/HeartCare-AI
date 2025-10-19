"""
HeartCare AI - FastAPI Backend
Lightweight API for cardiac arrest risk prediction
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import joblib
import pandas as pd
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="HeartCare AI API",
    description="Cardiac Arrest Risk Prediction API",
    version="2.0.0"
)

# CORS - Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model at startup
model = None

@app.on_event("startup")
async def load_model():
    """Load the trained model"""
    global model
    try:
        # Try local model first
        model_path = Path(__file__).parent / "cardiac_arrest_model.pkl"
        if model_path.exists():
            model = joblib.load(model_path)
            logger.info("✅ Model loaded from local file")
        else:
            # Download from Hugging Face if not found
            from huggingface_hub import hf_hub_download
            model_path = hf_hub_download(
                repo_id="ZainShahHere/cardiac_arrest_model",
                filename="cardiac_arrest_model.pkl"
            )
            model = joblib.load(model_path)
            logger.info("✅ Model downloaded and loaded from Hugging Face")
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        raise


# ============================================
# DATA MODELS
# ============================================

class PatientData(BaseModel):
    """15 input features for prediction"""
    # Personal (3)
    age: int = Field(..., ge=1, le=120)
    gender: str
    bmi: float = Field(..., ge=10.0, le=60.0)
    
    # Lifestyle (6)
    smoker: str
    physical_activity: str
    diet: str
    family_history: str
    stress_level: str
    alcohol_consumption: str
    
    # Clinical (6)
    diabetes: str
    hypertension: str
    cholesterol_level: float = 180
    sleep_hours: float = Field(..., ge=0.0, le=24.0)
    blood_pressure: int = Field(..., ge=60, le=200)
    blood_sugar: float = 90


class PredictionResponse(BaseModel):
    """Prediction output"""
    risk_percentage: int
    risk_category: str
    prediction: int
    confidence: float
    message: str
    recommendations: list


# ============================================
# HELPER FUNCTIONS
# ============================================

def impute_categorical(value: str, default: str = 'No') -> str:
    """Replace 'I don't know' with default value"""
    return default if value == "I don't know" else value


def get_risk_message(risk_pct: int, patient: PatientData) -> tuple:
    """Generate personalized message and recommendations"""
    recommendations = []
    
    # Base message by risk level
    if risk_pct < 20:
        message = "🎉 Great news! Your heart health looks good. Keep up the healthy lifestyle!"
        recommendations.append("✓ Continue your current healthy habits")
        recommendations.append("✓ Annual health checkups recommended")
    elif risk_pct < 50:
        message = "⚠️ Moderate risk detected. Some lifestyle improvements may help."
        recommendations.append("⚕️ Schedule a medical checkup soon")
        recommendations.append("📊 Monitor blood pressure and cholesterol regularly")
        recommendations.append("🏃 Increase physical activity to 30+ mins daily")
    else:
        message = "🚨 High risk detected. Please consult a healthcare professional immediately."
        recommendations.append("🚨 URGENT: Schedule medical consultation ASAP")
        recommendations.append("💊 Take prescribed medications regularly")
        recommendations.append("⚠️ Monitor symptoms: chest pain, shortness of breath")
    
    # Add specific recommendations based on lifestyle
    if patient.smoker == "Yes":
        recommendations.append("🚭 Quit smoking - critical for heart health")
    if patient.physical_activity == "Low":
        recommendations.append("🏃‍♂️ Start with 15-min daily walks")
    if patient.diet == "Unhealthy":
        recommendations.append("🥗 Focus on fruits, vegetables, whole grains")
    if patient.stress_level == "High":
        recommendations.append("🧘 Practice stress management techniques")
    if patient.bmi >= 30:
        recommendations.append("⚖️ Weight management can reduce risk significantly")
    if patient.sleep_hours < 6:
        recommendations.append("😴 Aim for 7-9 hours of sleep nightly")
    
    return message, recommendations


# ============================================
# API ENDPOINTS
# ============================================

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "healthy",
        "message": "HeartCare AI API is running!",
        "version": "2.0.0",
        "model_loaded": model is not None
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_risk(patient: PatientData):
    """
    🔮 Main prediction endpoint
    Takes 15 health features and returns risk assessment
    """
    try:
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Prepare features in correct order (must match training data)
        num_features = [
            patient.age,
            patient.bmi,
            patient.cholesterol_level,
            patient.sleep_hours,
            patient.blood_pressure,
            patient.blood_sugar
        ]
        
        cat_features = [
            impute_categorical(patient.gender, 'Male'),
            impute_categorical(patient.smoker, 'No'),
            impute_categorical(patient.diabetes, 'No'),
            impute_categorical(patient.hypertension, 'No'),
            impute_categorical(patient.physical_activity, 'Moderate'),
            impute_categorical(patient.diet, 'Healthy'),
            impute_categorical(patient.family_history, 'No'),
            impute_categorical(patient.stress_level, 'Moderate'),
            impute_categorical(patient.alcohol_consumption, 'No')
        ]
        
        # Create DataFrame
        feature_names = [
            'Age', 'BMI', 'Cholesterol_Level', 'Sleep_Hours', 'Blood_Pressure', 'Blood_Sugar',
            'Gender', 'Smoker', 'Diabetes', 'Hypertension', 'Physical_Activity',
            'Diet', 'Family_History', 'Stress_Level', 'Alcohol_Consumption'
        ]
        input_df = pd.DataFrame([num_features + cat_features], columns=feature_names)
        
        # Predict
        risk_prob = model.predict_proba(input_df)[0][1]
        risk_percentage = int(risk_prob * 100)
        prediction = model.predict(input_df)[0]
        risk_category = "High Risk" if prediction == 1 else "Low Risk"
        
        # Get personalized recommendations
        message, recommendations = get_risk_message(risk_percentage, patient)
        
        logger.info(f"✅ Prediction: {risk_percentage}% risk")
        
        return PredictionResponse(
            risk_percentage=risk_percentage,
            risk_category=risk_category,
            prediction=int(prediction),
            confidence=round(float(risk_prob), 3),
            message=message,
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"❌ Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    # Run the API server
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,  # Auto-reload on code changes (development only)
        log_level="info"
    )
