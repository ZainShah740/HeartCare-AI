"""
HeartCare AI - FastAPI Backend
Lightweight API for cardiac arrest risk prediction
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
import joblib
import pandas as pd
from pathlib import Path
import logging
import os

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

# Set Hugging Face cache to /tmp BEFORE any imports
os.environ['HF_HOME'] = '/tmp/huggingface'
os.environ['HUGGINGFACE_HUB_CACHE'] = '/tmp/huggingface/hub'

# Load model at startup
model = None

@app.on_event("startup")
async def load_model():
    """Load the trained model from Hugging Face"""
    global model
    try:
        logger.info("📥 Loading model from Hugging Face: ZainShahHere/cardiac_arrest_model")
        
        # Import after setting environment variables
        from huggingface_hub import hf_hub_download
        
        # Download model from your Hugging Face repository
        # This will use the /tmp cache we configured above
        model_path = hf_hub_download(
            repo_id="ZainShahHere/cardiac_arrest_model",
            filename="cardiac_arrest_model.pkl",
            repo_type="model"
        )
        
        logger.info(f"✅ Model downloaded to: {model_path}")
        model = joblib.load(model_path)
        logger.info("✅ Model successfully loaded from Hugging Face!")
        
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        logger.error(f"❌ Error type: {type(e).__name__}")
        import traceback
        logger.error(f"❌ Full traceback:\n{traceback.format_exc()}")
        raise RuntimeError(f"Could not load model from HuggingFace: {str(e)}")


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


def adjust_risk(predicted_risk, patient_data):
    """
    Balanced risk adjustment that respects model output while considering key factors.
    Strategy: Start with model, then apply small corrections based on critical factors.
    
    predicted_risk: float (0-100) - raw model output (PRIMARY source of truth)
    patient_data: PatientData object with all health information
    """
    
    # Count the 6 MOST CRITICAL risk factors
    critical_count = 0
    if patient_data.family_history == "Yes": critical_count += 1
    if patient_data.diabetes == "Yes": critical_count += 1
    if patient_data.hypertension == "Yes": critical_count += 1
    if patient_data.smoker == "Yes": critical_count += 1
    if patient_data.age >= 65: critical_count += 1
    if patient_data.cholesterol_level >= 240: critical_count += 1
    
    # Count protective factors (good health indicators)
    protective_count = 0
    if patient_data.age < 40: protective_count += 1
    if patient_data.physical_activity == "High": protective_count += 1
    if patient_data.diet == "Healthy": protective_count += 1
    if patient_data.smoker == "No": protective_count += 1
    if patient_data.bmi < 25: protective_count += 1
    if patient_data.stress_level == "Low": protective_count += 1
    
    # Calculate adjustment factor (subtle, not aggressive)
    # Range: 0.8 to 1.2 (only ±20% max adjustment)
    adjustment_factor = 1.0
    
    # If many critical factors BUT model says low risk → slight increase
    if critical_count >= 4 and predicted_risk < 50:
        adjustment_factor = 1.15  # Boost by 15%
    elif critical_count >= 3 and predicted_risk < 40:
        adjustment_factor = 1.10  # Boost by 10%
    
    # If many protective factors BUT model says high risk → slight decrease
    elif protective_count >= 5 and predicted_risk > 60:
        adjustment_factor = 0.85  # Reduce by 15%
    elif protective_count >= 4 and predicted_risk > 50:
        adjustment_factor = 0.90  # Reduce by 10%
    
    # If mixed signals (some critical + some protective) → trust model more
    elif critical_count >= 2 and protective_count >= 3:
        adjustment_factor = 1.0  # No adjustment, trust model
    
    # Apply adjustment
    adjusted_risk = predicted_risk * adjustment_factor
    
    # Safety bounds: never go below 10% or above 95%
    # (even perfect health has some risk, even worst health isn't 100%)
    adjusted_risk = min(max(adjusted_risk, 10), 95)
    
    return adjusted_risk

def risk_level(adjusted_risk):
    if adjusted_risk >= 70:
        return "High"
    elif adjusted_risk >= 40:
        return "Moderate"
    else:
        return "Low"

def get_risk_message(risk_pct: int, patient: PatientData) -> tuple:
    """Generate personalized message and recommendations"""
    recommendations = []
    if risk_pct < 40:
        message = "🎉 Great news! Your heart health looks good. Keep up the healthy lifestyle!"
        recommendations.append("✓ Continue your current healthy habits")
        recommendations.append("✓ Annual health checkups recommended")
    elif risk_pct < 70:
        message = "⚠️ Moderate risk detected. Some lifestyle improvements may help."
        recommendations.append("⚕️ Schedule a medical checkup soon")
        recommendations.append("📊 Monitor blood pressure and cholesterol regularly")
        recommendations.append("🏃 Increase physical activity to 30+ mins daily")
    else:
        message = "🚨 High risk detected. Please consult a healthcare professional immediately."
        recommendations.append("🚨 URGENT: Schedule medical consultation ASAP")
        recommendations.append("💊 Take prescribed medications regularly")
        recommendations.append("⚠️ Monitor symptoms: chest pain, shortness of breath")
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
    """Serve the frontend HTML"""
    html_path = Path(__file__).parent / "index.html"
    if html_path.exists():
        return FileResponse(html_path)
    return {
        "status": "healthy",
        "message": "HeartCare AI API is running!",
        "version": "2.0.0",
        "model_loaded": model is not None
    }

@app.get("/health")
async def health():
    """API health check endpoint"""
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
        raw_risk_percentage = float(risk_prob * 100)
        prediction = model.predict(input_df)[0]

        # Adjust risk based on comprehensive health profile
        adjusted_risk = adjust_risk(raw_risk_percentage, patient)
        risk_category = risk_level(adjusted_risk)

        # Get personalized recommendations
        message, recommendations = get_risk_message(int(adjusted_risk), patient)

        logger.info(f"✅ Prediction: {adjusted_risk:.1f}% risk (adjusted from {raw_risk_percentage:.1f}%)")

        return PredictionResponse(
            risk_percentage=int(round(adjusted_risk)),
            risk_category=f"{risk_category} Risk",
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
