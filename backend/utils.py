"""
HeartCare AI - Utility Functions
Helper functions for model loading, preprocessing, and recommendations
"""

import pandas as pd
import joblib
from pathlib import Path
import logging
from huggingface_hub import hf_hub_download

logger = logging.getLogger(__name__)

# Mode dictionary for imputation (default values)
MODE_DICT = {
    'Gender': 'Male',
    'Smoker': 'No',
    'Diabetes': 'No',
    'Hypertension': 'No',
    'Physical_Activity': 'Moderate',
    'Diet': 'Healthy',
    'Family_History': 'No',
    'Stress_Level': 'Moderate',
    'Alcohol_Consumption': 'No'
}


def get_model():
    """
    Load the trained model from local file or download from Hugging Face
    Returns the loaded model object
    """
    model_path = Path(__file__).parent / "cardiac_arrest_model.pkl"
    
    # Try to load local model first
    if model_path.exists():
        logger.info(f"Loading model from {model_path}")
        return joblib.load(model_path)
    
    # If not found locally, download from Hugging Face Hub
    try:
        logger.info("Model not found locally. Downloading from Hugging Face Hub...")
        downloaded_path = hf_hub_download(
            repo_id="ZainShahHere/cardiac_arrest_model",
            filename="cardiac_arrest_model.pkl",
            cache_dir=str(Path(__file__).parent)
        )
        logger.info(f"Model downloaded to {downloaded_path}")
        return joblib.load(downloaded_path)
    except Exception as e:
        logger.error(f"Failed to download model: {str(e)}")
        raise Exception("Could not load model. Please ensure model file exists or HF repo is accessible.")


def impute_categorical(feature_name, value):
    """
    Impute categorical features if user selects "I don't know"
    Uses mode (most common value) as default
    """
    if value == "I don't know":
        return MODE_DICT.get(feature_name, 'No')
    return value


def preprocess_input(patient_data):
    """
    Preprocess patient input data into the format expected by the model
    
    Args:
        patient_data: PatientData object with 15 features
    
    Returns:
        pd.DataFrame: Preprocessed data ready for model prediction
    """
    # Define feature order (must match training data)
    num_features = [
        'Age', 'BMI', 'Cholesterol_Level', 
        'Sleep_Hours', 'Blood_Pressure', 'Blood_Sugar'
    ]
    
    cat_features = [
        'Gender', 'Smoker', 'Diabetes', 'Hypertension',
        'Physical_Activity', 'Diet', 'Family_History',
        'Stress_Level', 'Alcohol_Consumption'
    ]
    
    # Extract and impute categorical features
    cat_values = [
        impute_categorical('Gender', patient_data.gender),
        impute_categorical('Smoker', patient_data.smoker),
        impute_categorical('Diabetes', patient_data.diabetes),
        impute_categorical('Hypertension', patient_data.hypertension),
        impute_categorical('Physical_Activity', patient_data.physical_activity),
        impute_categorical('Diet', patient_data.diet),
        impute_categorical('Family_History', patient_data.family_history),
        impute_categorical('Stress_Level', patient_data.stress_level),
        impute_categorical('Alcohol_Consumption', patient_data.alcohol_consumption)
    ]
    
    # Extract numerical features
    num_values = [
        patient_data.age,
        patient_data.bmi,
        patient_data.cholesterol_level,
        patient_data.sleep_hours,
        patient_data.blood_pressure,
        patient_data.blood_sugar
    ]
    
    # Combine into DataFrame (order matters!)
    all_values = num_values + cat_values
    all_features = num_features + cat_features
    
    input_df = pd.DataFrame([all_values], columns=all_features)
    
    return input_df


def get_risk_message(risk_percentage, patient_data):
    """
    Generate personalized health message and recommendations based on risk level
    
    Args:
        risk_percentage: Risk percentage (0-100)
        patient_data: PatientData object
    
    Returns:
        tuple: (message, recommendations list)
    """
    recommendations = []
    
    # Risk-based message
    if risk_percentage < 20:
        message = "🎉 Great news! Your heart health looks good. Keep up the healthy lifestyle!"
        recommendations.append("Continue your current healthy habits")
        recommendations.append("Regular exercise and balanced diet are key")
        recommendations.append("Annual health checkups recommended")
    elif risk_percentage < 50:
        message = "⚠️ Moderate risk detected. Some lifestyle improvements may help reduce your risk."
        recommendations.append("Consider scheduling a medical checkup")
        recommendations.append("Monitor your blood pressure and cholesterol regularly")
        recommendations.append("Increase physical activity to 30+ mins daily")
    else:
        message = "🚨 High risk detected. Please consult a healthcare professional soon."
        recommendations.append("⚕️ URGENT: Schedule a medical consultation immediately")
        recommendations.append("Monitor symptoms like chest pain, shortness of breath")
        recommendations.append("Avoid strenuous activities until cleared by doctor")
        recommendations.append("Take prescribed medications regularly")
    
    # Lifestyle-specific recommendations
    if patient_data.smoker == "Yes":
        recommendations.append("🚭 Quit smoking - it's the single best thing for your heart")
    
    if patient_data.physical_activity == "Low":
        recommendations.append("🏃‍♂️ Start with 15-minute daily walks, gradually increase")
    
    if patient_data.diet == "Unhealthy":
        recommendations.append("🥗 Focus on fruits, vegetables, whole grains, and lean proteins")
    
    if patient_data.stress_level == "High":
        recommendations.append("🧘‍♀️ Practice stress management: meditation, yoga, or deep breathing")
    
    if patient_data.bmi >= 30:
        recommendations.append("⚖️ Weight management through diet and exercise can reduce risk")
    
    if patient_data.sleep_hours < 6:
        recommendations.append("😴 Aim for 7-9 hours of quality sleep per night")
    
    if patient_data.alcohol_consumption == "Yes":
        recommendations.append("🍷 Limit alcohol consumption to moderate levels")
    
    # Clinical recommendations
    if patient_data.hypertension == "Yes":
        recommendations.append("💊 Keep blood pressure under control with medication and lifestyle")
    
    if patient_data.diabetes == "Yes":
        recommendations.append("🩸 Manage blood sugar levels through diet, exercise, and medication")
    
    if patient_data.cholesterol_level > 240:
        recommendations.append("📊 High cholesterol - discuss statin therapy with your doctor")
    
    return message, recommendations


def get_feature_importance():
    """
    Get feature importance from the trained model (for future use)
    Can be used to show users which factors most influenced their prediction
    """
    # This would require extracting feature importance from the RandomForest
    # Left as placeholder for future enhancement
    pass
