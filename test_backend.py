"""
Test script to verify HeartCare AI backend is working
Run this after starting the backend server
"""

import requests
import json

# Configuration
API_URL = "http://localhost:8000"

def test_health_check():
    """Test if backend is running"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            print("✅ Backend is running!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("   Make sure backend is running on http://localhost:8000")
        return False


def test_prediction():
    """Test prediction endpoint with sample data"""
    print("\n🔮 Testing prediction endpoint...")
    
    # Sample patient data (low risk profile)
    sample_data = {
        "age": 30,
        "gender": "Male",
        "bmi": 22.0,
        "smoker": "No",
        "physical_activity": "High",
        "diet": "Healthy",
        "family_history": "No",
        "stress_level": "Low",
        "alcohol_consumption": "No",
        "diabetes": "No",
        "hypertension": "No",
        "cholesterol_level": 180,
        "sleep_hours": 7.0,
        "blood_pressure": 120,
        "blood_sugar": 90
    }
    
    try:
        response = requests.post(f"{API_URL}/predict", json=sample_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction successful!")
            print(f"   Risk: {result['risk_percentage']}%")
            print(f"   Category: {result['risk_category']}")
            print(f"   Confidence: {result['confidence']}")
            print(f"   Message: {result['message']}")
            print(f"   Recommendations: {len(result['recommendations'])} items")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False


def test_high_risk_prediction():
    """Test with high risk profile"""
    print("\n🚨 Testing high-risk prediction...")
    
    # High risk patient data
    high_risk_data = {
        "age": 55,
        "gender": "Male",
        "bmi": 32.0,
        "smoker": "Yes",
        "physical_activity": "Low",
        "diet": "Unhealthy",
        "family_history": "Yes",
        "stress_level": "High",
        "alcohol_consumption": "Yes",
        "diabetes": "Yes",
        "hypertension": "Yes",
        "cholesterol_level": 260,
        "sleep_hours": 5.0,
        "blood_pressure": 150,
        "blood_sugar": 140
    }
    
    try:
        response = requests.post(f"{API_URL}/predict", json=high_risk_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ High-risk prediction successful!")
            print(f"   Risk: {result['risk_percentage']}%")
            print(f"   Category: {result['risk_category']}")
            return True
        else:
            print(f"❌ High-risk prediction failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ High-risk prediction error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("HeartCare AI - Backend Test Suite")
    print("=" * 50)
    
    tests_passed = 0
    tests_total = 3
    
    # Run tests
    if test_health_check():
        tests_passed += 1
    
    if test_prediction():
        tests_passed += 1
    
    if test_high_risk_prediction():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"Test Results: {tests_passed}/{tests_total} passed")
    print("=" * 50)
    
    if tests_passed == tests_total:
        print("🎉 All tests passed! Backend is working correctly.")
        print("✅ You can now start the frontend and test the full application.")
    else:
        print("⚠️ Some tests failed. Check the error messages above.")
        print("💡 Make sure the backend is running: python backend/main.py")


if __name__ == "__main__":
    main()
