<template>
  <div id="app">
    <!-- Header -->
    <header class="app-header">
      <div class="header-content">
        <div class="logo">
          <span class="logo-icon">❤️</span>
          <h1>HeartCare AI</h1>
        </div>
        <p class="tagline">AI-Powered Cardiac Arrest Risk Prediction</p>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Info Banner -->
      <div class="info-banner">
        <div class="alert alert-info">
          <span>ℹ️</span>
          <div>
            <strong>Why Heart Health Matters:</strong> Heart disease is the leading cause of death worldwide. 
            Early risk prediction can save lives. Use this tool to understand your risk and take action.
          </div>
        </div>
      </div>

      <!-- Prediction Form or Results -->
      <PredictionForm 
        v-if="!showResults" 
        @submit="handlePrediction"
        :loading="loading"
      />
      
      <ResultsDisplay 
        v-else 
        :results="predictionResults"
        @reset="resetForm"
      />
    </main>

    <!-- Footer -->
    <footer class="app-footer">
      <p>HeartCare AI © 2025 | Built with ❤️ for Pakistan | 
        <a href="https://github.com/ZainShah6500/HeartCareAI-UraanAI" target="_blank">GitHub</a>
      </p>
      <p class="disclaimer">
        <small>⚠️ Disclaimer: This tool is for informational purposes only and should not replace professional medical advice.</small>
      </p>
    </footer>
  </div>
</template>

<script>
import { ref } from 'vue'
import PredictionForm from './components/PredictionForm.vue'
import ResultsDisplay from './components/ResultsDisplay.vue'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    PredictionForm,
    ResultsDisplay
  },
  setup() {
    const loading = ref(false)
    const showResults = ref(false)
    const predictionResults = ref(null)

    // Simple API URL configuration
    const API_URL = 'http://localhost:8000'

    const handlePrediction = async (formData) => {
      loading.value = true
      showResults.value = false

      try {
        // Call FastAPI /predict endpoint
        const response = await axios.post(`${API_URL}/predict`, formData)
        
        predictionResults.value = response.data
        showResults.value = true
        
        // Smooth scroll to results
        setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100)

      } catch (error) {
        console.error('❌ Prediction error:', error)
        const errorMsg = error.response?.data?.detail || 'Connection failed. Is the backend running?'
        alert(`Error: ${errorMsg}`)
      } finally {
        loading.value = false
      }
    }

    const resetForm = () => {
      showResults.value = false
      predictionResults.value = null
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    return {
      loading,
      showResults,
      predictionResults,
      handlePrediction,
      resetForm
    }
  }
}
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-dark) 100%);
  color: var(--white);
  padding: var(--spacing-xl) var(--spacing-lg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  margin-bottom: var(--spacing-lg);
  text-align: center;
}

.header-content {
  max-width: 800px;
  margin: 0 auto;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
}

.logo-icon {
  font-size: 3rem;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.logo h1 {
  color: var(--white);
  margin: 0;
  font-size: var(--font-size-2xl);
}

.tagline {
  font-size: var(--font-size-lg);
  opacity: 0.95;
  margin: 0;
}

.info-banner {
  margin-bottom: var(--spacing-lg);
}

.main-content {
  min-height: 60vh;
}

.app-footer {
  margin-top: var(--spacing-xl);
  padding: var(--spacing-lg);
  text-align: center;
  color: var(--dark-gray);
  border-top: 2px solid var(--light-gray);
}

.app-footer a {
  color: var(--primary-blue);
  text-decoration: none;
  font-weight: 600;
}

.app-footer a:hover {
  text-decoration: underline;
}

.disclaimer {
  margin-top: var(--spacing-sm);
  color: var(--danger-red);
}

@media (max-width: 768px) {
  .app-header {
    padding: var(--spacing-lg) var(--spacing-md);
  }
  
  .logo-icon {
    font-size: 2rem;
  }
  
  .logo h1 {
    font-size: var(--font-size-xl);
  }
  
  .tagline {
    font-size: var(--font-size-base);
  }
}
</style>
