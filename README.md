# ❤️ HeartCare AI - Cardiac Arrest Risk Predictor

> **AI-Powered Heart Disease Risk Assessment | FastAPI + Vue.js**

Professional full-stack web app that predicts cardiac arrest risk using Machine Learning (85% accuracy, trained on 400K+ records). Designed for **Pakistan's healthcare challenges** with instant, accessible insights.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![Vue.js 3](https://img.shields.io/badge/Vue.js-3.5-brightgreen.svg)](https://vuejs.org/)

**✨ Competition-Ready | 🚀 Easy Setup | 💡 Real-World Impact**

---

## 🌟 Key Features

| Feature | Description |
|---------|-------------|
| 🎯 **85% Accuracy** | Random Forest model trained on 400K+ Pakistan patient records |
| 🎨 **Modern UI** | Medical-tech theme with blue/white colors, fully responsive |
| 📊 **Smart Recommendations** | Personalized health advice based on 15 input features |
| 🔒 **Privacy First** | No data storage, all predictions run locally |
| ⚡ **Lightning Fast** | Instant predictions via FastAPI backend |
| 📱 **Mobile Ready** | Works perfectly on all devices |
| 📄 **Export Reports** | Download risk assessment as text file |

---

## 🏗️ Project Structure

```
HeartCareAI/
├── backend/                    # FastAPI Backend
│   ├── main.py                # API endpoints and server logic
│   ├── utils.py               # Helper functions (preprocessing, recommendations)
│   ├── requirements.txt       # Python dependencies
│   └── download_model.py      # Script to download model from HuggingFace
│
├── frontend/                   # Vue.js Frontend
│   ├── src/
│   │   ├── App.vue           # Main application component
│   │   ├── components/
│   │   │   ├── PredictionForm.vue    # Input form for health data
│   │   │   └── ResultsDisplay.vue    # Risk results and recommendations
│   │   ├── main.js           # Vue app entry point
│   │   └── style.css         # Global styles
│   ├── public/               # Static assets
│   ├── index.html            # HTML template
│   ├── package.json          # Node dependencies
│   ├── vite.config.js        # Vite configuration
│   └── nginx.conf            # Nginx config for production
│
├── Heart_Disease_Prediction.ipynb  # Jupyter notebook (model training)
├── heart_data.csv            # Dataset (400K records)
├── heart_app.py              # Legacy Streamlit app
├── requirements.txt          # Legacy dependencies
│
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
└── README.md                # This file
```

---

## 🚀 Quick Start (3 Minutes!)

### Prerequisites
- Python 3.11+ 
- Node.js 20+ 
- Git

---

### ⚡ Setup & Run

#### **Step 1: Clone Repository**
```bash
git clone https://github.com/ZainShah740/HeartCareAI-UraanAI.git
cd HeartCareAI-UraanAI
```

#### **Step 2: Backend (Terminal 1)**
```bash
# Install dependencies
cd backend
pip install fastapi uvicorn joblib pandas scikit-learn huggingface-hub

# Download model from Hugging Face
python download_model.py

# Start backend server
python main.py
```
✅ **Backend running at: http://localhost:8000**  
📄 **API docs at: http://localhost:8000/docs**

---

#### **Step 3: Frontend (Terminal 2)**
```bash
# Install dependencies
cd frontend
npm install

# Start frontend
npm run dev
```
✅ **Frontend running at: http://localhost:3000**

---

### 🎉 That's It!
Open **http://localhost:3000** in your browser and start predicting! 

---

## 🐳 Docker Deployment

### Option 1: Docker Compose (Recommended)

```bash
# Build and run both services
docker-compose up --build

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Option 2: Individual Containers

```bash
# Build backend
docker build -f Dockerfile.backend -t heartcare-backend .
docker run -p 8000:8000 heartcare-backend

# Build frontend
docker build -f Dockerfile.frontend -t heartcare-frontend .
docker run -p 3000:80 heartcare-frontend
```

---

## 🌐 Deployment

### Deploy on **Hugging Face Spaces**

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces)
2. Select **Docker** as SDK
3. Push your code to the Space repository
4. The `spaces_config.yml` will handle the configuration

### Deploy on **Render**

1. Create a new **Web Service** on [Render](https://render.com)
2. Connect your GitHub repository
3. Set build command: `pip install -r backend/requirements.txt`
4. Set start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. For frontend, create a **Static Site** pointing to `frontend/dist/`

---

## 📊 Model & Input Features

### 🧠 Model Performance
| Metric | Value |
|--------|-------|
| **Algorithm** | Calibrated Random Forest Classifier |
| **Accuracy** | 85% |
| **ROC-AUC** | 0.926 |
| **Training Data** | 400K+ Pakistan patient records |

### 📝 15 Input Features

| Category | Features |
|----------|----------|
| **👤 Personal (3)** | Age, Gender, BMI |
| **🏠 Lifestyle (6)** | Smoker, Physical Activity, Diet, Family History, Stress Level, Alcohol |
| **🩺 Clinical (6)** | Diabetes, Hypertension, Cholesterol, Sleep Hours, Blood Pressure, Blood Sugar |

---

## 🔌 API Quick Reference

### Main Endpoint: `POST /predict`

**Input Example:**
```json
{
  "age": 30, "gender": "Male", "bmi": 22.0,
  "smoker": "No", "physical_activity": "High", "diet": "Healthy",
  "family_history": "No", "stress_level": "Low", 
  "alcohol_consumption": "No", "diabetes": "No", "hypertension": "No",
  "cholesterol_level": 180, "sleep_hours": 7.0,
  "blood_pressure": 120, "blood_sugar": 90
}
```

**Output Example:**
```json
{
  "risk_percentage": 11,
  "risk_category": "Low Risk",
  "prediction": 0,
  "confidence": 0.89,
  "message": "🎉 Great news! Your heart health looks good...",
  "recommendations": ["✓ Continue healthy habits", "✓ Annual checkups recommended"]
}
```

📚 **Full API Docs:** http://localhost:8000/docs (when backend is running)

---

## 🎨 User Interface

### 🏠 Home Screen
Professional medical-tech design with **blue/white color theme**

### 📝 Prediction Form
- **3 Sections**: Personal Info, Lifestyle, Clinical Indicators
- **15 Input Fields**: All clearly labeled with helpful hints
- **Smart Validation**: Real-time input checking

### 📊 Results Display
- **Risk Gauge**: Circular percentage display (color-coded: green/yellow/red)
- **Status Badge**: "At Risk" or "Safe"
- **Personalized Message**: Based on your risk level
- **Smart Recommendations**: Tailored health tips
- **Health Tips Grid**: General heart health advice
- **Download Report**: Export as .txt file

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Connect & Support

**Developer**: Zain Shah

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/zain-shah-871aa532a)
[![Twitter](https://img.shields.io/badge/Twitter-Follow-blue?logo=twitter)](https://x.com/zainshah_x)
[![Email](https://img.shields.io/badge/Email-Contact-red?logo=gmail)](mailto:btenmeten12345@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/ZainShah6500)

---

## ⚠️ Disclaimer

**This tool is for informational and educational purposes only.** It should **NOT** replace professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical decisions.

---

## 🙏 Acknowledgments

- **Dataset**: Kaggle - Pakistan Heart Attack Risk Dataset
- **Inspiration**: Addressing Pakistan's rising cardiac health challenges
- **Technologies**: FastAPI, Vue.js, scikit-learn, Hugging Face Hub

---

## 📈 Roadmap

- [ ] Add user authentication and history tracking
- [ ] Integrate with wearable devices (Fitbit, Apple Watch)
- [ ] Multi-language support (Urdu, Punjabi)
- [ ] Real-time monitoring dashboard
- [ ] Mobile app (React Native)
- [ ] Integration with telemedicine platforms

---

**Built with ❤️ for Pakistan | HeartCare AI © 2025**


