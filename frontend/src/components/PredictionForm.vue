<template>
  <div class="prediction-form">
    <div class="card">
      <div class="card-header text-center">
        <h2>Enter Your Health Information</h2>
        <p>Fill in your details below to assess your cardiac arrest risk</p>
      </div>

      <form @submit.prevent="submitForm">
        <!-- Personal Information Section -->
        <section class="form-section">
          <h3 class="section-title">👤 Personal Information</h3>
          <div class="grid grid-2">
            <div class="form-group">
              <label class="form-label" for="age">Age *</label>
              <input
                type="number"
                id="age"
                v-model.number="formData.age"
                class="form-input"
                min="1"
                max="120"
                required
                placeholder="Enter your age"
              />
            </div>

            <div class="form-group">
              <label class="form-label" for="gender">Gender *</label>
              <select
                id="gender"
                v-model="formData.gender"
                class="form-select"
                required
              >
                <option value="">Select gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="I don't know">I don't know</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label" for="bmi">BMI (Body Mass Index) *</label>
              <input
                type="number"
                id="bmi"
                v-model.number="formData.bmi"
                class="form-input"
                min="10"
                max="60"
                step="0.1"
                required
                placeholder="e.g., 22.5"
              />
              <small class="form-hint">Calculate: Weight(kg) ÷ Height²(m)</small>
            </div>
          </div>
        </section>

        <!-- Lifestyle & Habits Section -->
        <section class="form-section">
          <h3 class="section-title">🏠 Lifestyle & Habits</h3>
          <div class="grid grid-2">
            <div class="form-group">
              <label class="form-label" for="smoker">Smoker *</label>
              <select
                id="smoker"
                v-model="formData.smoker"
                class="form-select"
                required
              >
                <option value="">Select</option>
                <option value="Yes">Yes</option>
                <option value="No">No</option>
                <option value="I don't know">I don't know</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label" for="physical_activity">Physical Activity *</label>
              <select
                id="physical_activity"
                v-model="formData.physical_activity"
                class="form-select"
                required
              >
                <option value="">Select activity level</option>
                <option value="High">High (Regular exercise)</option>
                <option value="Moderate">Moderate (Some exercise)</option>
                <option value="Low">Low (Minimal exercise)</option>
                <option value="I don't know">I don't know</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label" for="diet">Diet Quality *</label>
              <select
                id="diet"
                v-model="formData.diet"
                class="form-select"
                required
              >
                <option value="">Select diet type</option>
                <option value="Healthy">Healthy (Balanced, nutritious)</option>
                <option value="Unhealthy">Unhealthy (Processed foods)</option>
                <option value="I don't know">I don't know</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label" for="family_history">Family History of Heart Disease *</label>
              <select
                id="family_history"
                v-model="formData.family_history"
                class="form-select"
                required
              >
                <option value="">Select</option>
                <option value="Yes">Yes</option>
                <option value="No">No</option>
                <option value="I don't know">I don't know</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label" for="stress_level">Stress Level *</label>
              <select
                id="stress_level"
                v-model="formData.stress_level"
                class="form-select"
                required
              >
                <option value="">Select stress level</option>
                <option value="High">High</option>
                <option value="Moderate">Moderate</option>
                <option value="Low">Low</option>
                <option value="I don't know">I don't know</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label" for="alcohol_consumption">Alcohol Consumption *</label>
              <select
                id="alcohol_consumption"
                v-model="formData.alcohol_consumption"
                class="form-select"
                required
              >
                <option value="">Select</option>
                <option value="Yes">Yes</option>
                <option value="No">No</option>
                <option value="I don't know">I don't know</option>
              </select>
            </div>
          </div>
        </section>

        <!-- Clinical Indicators Section -->
        <section class="form-section">
          <h3 class="section-title">🩺 Clinical Indicators</h3>
          <div class="grid grid-2">
            <div class="form-group">
              <label class="form-label" for="diabetes">Diabetes *</label>
              <select
                id="diabetes"
                v-model="formData.diabetes"
                class="form-select"
                required
              >
                <option value="">Select</option>
                <option value="Yes">Yes</option>
                <option value="No">No</option>
                <option value="I don't know">I don't know</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label" for="hypertension">Hypertension (High BP) *</label>
              <select
                id="hypertension"
                v-model="formData.hypertension"
                class="form-select"
                required
              >
                <option value="">Select</option>
                <option value="Yes">Yes</option>
                <option value="No">No</option>
                <option value="I don't know">I don't know</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label" for="cholesterol_level">Cholesterol Level (mg/dL)</label>
              <input
                type="number"
                id="cholesterol_level"
                v-model.number="formData.cholesterol_level"
                class="form-input"
                min="100"
                max="400"
                placeholder="e.g., 180 (optional)"
              />
              <small class="form-hint">Leave blank if unknown (default: 180)</small>
            </div>

            <div class="form-group">
              <label class="form-label" for="sleep_hours">Sleep Hours per Night *</label>
              <input
                type="number"
                id="sleep_hours"
                v-model.number="formData.sleep_hours"
                class="form-input"
                min="0"
                max="24"
                step="0.5"
                required
                placeholder="e.g., 7.5"
              />
            </div>

            <div class="form-group">
              <label class="form-label" for="blood_pressure">Blood Pressure (Systolic) *</label>
              <input
                type="number"
                id="blood_pressure"
                v-model.number="formData.blood_pressure"
                class="form-input"
                min="60"
                max="200"
                required
                placeholder="e.g., 120"
              />
              <small class="form-hint">Systolic BP (top number)</small>
            </div>

            <div class="form-group">
              <label class="form-label" for="blood_sugar">Blood Sugar (mg/dL)</label>
              <input
                type="number"
                id="blood_sugar"
                v-model.number="formData.blood_sugar"
                class="form-input"
                min="50"
                max="300"
                placeholder="e.g., 90 (optional)"
              />
              <small class="form-hint">Leave blank if unknown (default: 90)</small>
            </div>
          </div>
        </section>

        <!-- Submit Button -->
        <div class="form-actions text-center">
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="loading"
          >
            <span v-if="!loading">🔍 Predict My Risk</span>
            <span v-else>
              <span class="spinner-inline"></span>
              Analyzing...
            </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'

export default {
  name: 'PredictionForm',
  props: {
    loading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['submit'],
  setup(props, { emit }) {
    // Form data with default values
    const formData = reactive({
      age: 30,
      gender: '',
      bmi: 22.0,
      smoker: '',
      physical_activity: '',
      diet: '',
      family_history: '',
      stress_level: '',
      alcohol_consumption: '',
      diabetes: '',
      hypertension: '',
      cholesterol_level: 180,
      sleep_hours: 7.0,
      blood_pressure: 120,
      blood_sugar: 90
    })

    const submitForm = () => {
      // Validate form
      const requiredFields = [
        'age', 'gender', 'bmi', 'smoker', 'physical_activity',
        'diet', 'family_history', 'stress_level', 'alcohol_consumption',
        'diabetes', 'hypertension', 'sleep_hours', 'blood_pressure'
      ]

      const isValid = requiredFields.every(field => formData[field] !== '' && formData[field] !== null)

      if (!isValid) {
        alert('Please fill in all required fields marked with *')
        return
      }

      // Emit form data to parent
      emit('submit', { ...formData })
    }

    return {
      formData,
      submitForm
    }
  }
}
</script>

<style scoped>
.prediction-form {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.form-section {
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-lg);
  border-bottom: 2px solid var(--light-gray);
}

.form-section:last-of-type {
  border-bottom: none;
}

.section-title {
  color: var(--primary-blue);
  font-size: var(--font-size-lg);
  margin-bottom: var(--spacing-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.form-hint {
  display: block;
  color: var(--dark-gray);
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.form-actions {
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-lg);
}

.spinner-inline {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid var(--white);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-right: 0.5rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Form styling improvements */
.form-input:hover,
.form-select:hover {
  border-color: var(--primary-light);
}

.form-input:invalid,
.form-select:invalid {
  border-color: var(--danger-red);
}

@media (max-width: 768px) {
  .grid-2 {
    grid-template-columns: 1fr;
  }
}
</style>
