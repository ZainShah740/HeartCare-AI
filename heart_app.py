# Modern Streamlit Heart Disease Risk Prediction MVP
import streamlit as st
import numpy as np
import pandas as pd
import joblib
import shap
from huggingface_hub import hf_hub_download



# Download model file from Hugging Face Hub with caching
@st.cache_data
def get_model_path():
	return hf_hub_download(
		repo_id="ZainShahHere/cardiac_arrest_model",  # your model repo
		filename="cardiac_arrest_model.pkl"      # exact file name you uploaded
	)

model_path = get_model_path()
calibrated_rf = joblib.load(model_path)



# Load model
# @st.cache_resource
# def load_model():
# 	return joblib.load('cardiac_arrest_model.pkl')
# calibrated_rf = load_model()

# Example: cache data loading if you use a CSV or heavy preprocessing
# @st.cache_data
# def load_data():
# 	return pd.read_csv('heart_data.csv')
# df = load_data()  # Uncomment if you use the dataset in the app

# Feature lists
num_features = ['Age', 'BMI', 'Cholesterol_Level', 'Sleep_Hours', 'Blood_Pressure', 'Blood_Sugar']
cat_features = ['Gender', 'Smoker', 'Diabetes', 'Hypertension', 'Physical_Activity', 'Diet', 'Family_History', 'Stress_Level', 'Alcohol_Consumption']

# Imputation function for categorical features
def impute_cat(feature, value, mode_dict):
	if value == "I don't know":
		return mode_dict.get(feature, 'No')
	return value

# UI Styling

st.set_page_config(page_title="Heart Disease Risk Predictor", page_icon="❤️", layout="wide")
st.markdown("""
	<style>
	.main {background-color: #f7f9fa;}
	.stApp {background-color: #f7f9fa;}
	.sidebar .sidebar-content {background: linear-gradient(135deg, #e0f7fa 0%, #fff 100%);}
	.stButton>button {background-color: #ff4b4b; color: white; font-weight: bold;}
	</style>
	""", unsafe_allow_html=True)

# Sidebar visuals and info
with st.sidebar:
	st.markdown("### Why Heart Health Matters")
	st.write("Heart disease is the leading cause of death worldwide. Early risk prediction can save lives. Use this tool to understand your risk and take action.")
	st.markdown("---")
	st.markdown("**Tip:** Regular checkups and a healthy lifestyle are key to prevention.")

st.title("Heart Disease Risk Predictor")
st.subheader("Empowering You to Take Control of Your Heart Health")
st.markdown("Enter your health details below. The app predicts your risk of cardiac arrest using AI.")

# Mode dictionary for imputation (can be updated with real mode values)
mode_dict = {f: 'No' for f in cat_features}

# Input form
with st.form("input_form"):
	with st.expander("👤 Personal Information", expanded=True):
		age = st.number_input("Age", min_value=1, max_value=120, value=30, key="age")
		gender = st.selectbox("Gender", ["Male", "Female", "I don't know"], key="gender")
		bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=22.0, key="bmi")

	with st.expander("🏠 Lifestyle & Habits", expanded=True):
		smoker = st.selectbox("Smoker", ["Yes", "No", "I don't know"], key="smoker")
		activity = st.selectbox("Physical Activity", ["High", "Moderate", "Low", "I don't know"], key="activity")
		diet = st.selectbox("Diet", ["Healthy", "Unhealthy", "I don't know"], key="diet")
		family = st.selectbox("Family History", ["Yes", "No", "I don't know"], key="family")
		stress = st.selectbox("Stress Level", ["High", "Moderate", "Low", "I don't know"], key="stress")
		alcohol = st.selectbox("Alcohol Consumption", ["Yes", "No", "I don't know"], key="alcohol")

	with st.expander("🩺 Clinical Indicators", expanded=True):
		diabetes = st.selectbox("Diabetes", ["Yes", "No", "I don't know"], key="diabetes")
		hypertension = st.selectbox("Hypertension", ["Yes", "No", "I don't know"], key="hypertension")
		chol_choice = st.selectbox("Do you know your Cholesterol Level?", ["Yes", "I don't know"], key="chol_choice")
		if chol_choice == "Yes":
			chol = st.number_input("Cholesterol Level", min_value=100, max_value=400, value=180, key="cholesterol_level")
		else:
			chol = 180  # Impute with median or typical value

		sleep = st.number_input("Sleep Hours", min_value=0.0, max_value=24.0, value=7.0, key="sleep_hours")
		bp = st.number_input("Blood Pressure", min_value=60, max_value=200, value=120, key="blood_pressure")

		sugar_choice = st.selectbox("Do you know your Blood Sugar?", ["Yes", "I don't know"], key="sugar_choice")
		if sugar_choice == "Yes":
			sugar = st.number_input("Blood Sugar", min_value=50, max_value=300, value=90, key="blood_sugar")
		else:
			sugar = 90  # Impute with median or typical value


	submit = st.form_submit_button("Predict My Risk")

if submit:
	# Impute categorical features
	cat_inputs = [
		impute_cat('Gender', gender, mode_dict),
		impute_cat('Smoker', smoker, mode_dict),
		impute_cat('Diabetes', diabetes, mode_dict),
		impute_cat('Hypertension', hypertension, mode_dict),
		impute_cat('Physical_Activity', activity, mode_dict),
		impute_cat('Diet', diet, mode_dict),
		impute_cat('Family_History', family, mode_dict),
		impute_cat('Stress_Level', stress, mode_dict),
		impute_cat('Alcohol_Consumption', alcohol, mode_dict)
	]
	num_inputs = [age, bmi, chol, sleep, bp, sugar]
	input_df = pd.DataFrame([num_inputs + cat_inputs], columns=num_features + cat_features)

	# Only run prediction inside button
	risk_prob = calibrated_rf.predict_proba(input_df)[0][1]
	risk_pct = int(risk_prob * 100)
	prediction = calibrated_rf.predict(input_df)[0]

	st.markdown(f"## Your heart is <span style='color:red'>{risk_pct}%</span> at risk of cardiac arrest.", unsafe_allow_html=True)
	st.markdown(f"### AI Prediction: {'High Risk' if prediction == 1 else 'Low Risk'}")
