# ⚡ HeartCare AI - Quick Start Guide

## 🎯 For Judges & Reviewers

This is a **competition-ready** AI application. Follow these steps to run it locally in **3 minutes**.

---

## ✅ What You'll Get

- **FastAPI Backend** running on http://localhost:8000
- **Vue.js Frontend** running on http://localhost:3000
- **Interactive API docs** at http://localhost:8000/docs
- **Live heart risk predictions** with personalized recommendations

---

## 🚀 Setup Instructions

### Prerequisites
```bash
python --version   # Should be 3.11+
node --version     # Should be 20+
```

---

### Step 1: Backend (Terminal 1)

```powershell
# Navigate to backend
cd backend

# Install Python dependencies (one-time)
pip install fastapi uvicorn joblib pandas scikit-learn huggingface-hub

# Download trained model from Hugging Face (one-time)
python download_model.py

# Start backend server
python main.py
```

**✅ Backend ready at:** http://localhost:8000  
**📚 API docs at:** http://localhost:8000/docs

---

### Step 2: Frontend (Terminal 2 - New Window)

```powershell
# Navigate to frontend
cd frontend

# Install Node dependencies (one-time)
npm install

# Start development server
npm run dev
```

**✅ Frontend ready at:** http://localhost:3000

---

## 🧪 Test the Application

### Option 1: Web Interface
1. Open http://localhost:3000
2. Fill in the health form (15 fields)
3. Click "Predict My Risk"
4. View results with personalized recommendations

### Option 2: Direct API Test
1. Open http://localhost:8000/docs
2. Try the `/predict` endpoint with this sample:

```json
{
  "age": 45,
  "gender": "Male",
  "bmi": 28.5,
  "smoker": "Yes",
  "physical_activity": "Low",
  "diet": "Unhealthy",
  "family_history": "Yes",
  "stress_level": "High",
  "alcohol_consumption": "Yes",
  "diabetes": "No",
  "hypertension": "Yes",
  "cholesterol_level": 240,
  "sleep_hours": 5.5,
  "blood_pressure": 145,
  "blood_sugar": 110
}
```

Expected output: **High risk** with detailed recommendations

---

## 🛠️ Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`  
**Solution:** 
```bash
pip install -r backend/requirements.txt
```

**Problem:** Model not found  
**Solution:** 
```bash
cd backend
python download_model.py
```

### Frontend Issues

**Problem:** `npm install` fails  
**Solution:** 
```bash
npm cache clean --force
npm install
```

**Problem:** Connection refused to backend  
**Solution:** Make sure backend is running on port 8000

---

## 📊 Key Features to Test

1. **Risk Calculation**: Try different input combinations
2. **Color Coding**: 
   - Green circle = Low risk (<20%)
   - Yellow circle = Moderate risk (20-50%)
   - Red circle = High risk (>50%)
3. **Smart Recommendations**: Vary lifestyle factors to see different advice
4. **Download Report**: Export your risk assessment
5. **Responsive Design**: Try on mobile/tablet

---

## 🎓 Model Details

- **Algorithm**: Calibrated Random Forest
- **Accuracy**: 85%
- **Training Data**: 400K+ Pakistan patient records
- **Features**: 15 inputs (personal, lifestyle, clinical)
- **Output**: Risk percentage + personalized recommendations

---

## 📞 Support

**Developer**: Zain Shah  
**GitHub**: https://github.com/ZainShah6500/HeartCareAI-UraanAI  
**LinkedIn**: https://www.linkedin.com/in/zain-shah-871aa532a

---

## ⚡ Quick Commands Reference

```bash
# Backend
cd backend
python main.py

# Frontend (new terminal)
cd frontend
npm run dev

# Stop servers
Ctrl+C in each terminal
```

---

**🎉 That's it! You're ready to explore HeartCare AI.**
