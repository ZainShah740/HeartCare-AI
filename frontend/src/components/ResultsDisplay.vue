<template>
  <div class="results-display">
    <!-- Risk Score Card -->
    <div class="card result-card">
      <div class="risk-header text-center">
        <div class="risk-icon">
          <span v-if="results.risk_percentage < 20">✅</span>
          <span v-else-if="results.risk_percentage < 50">⚠️</span>
          <span v-else>🚨</span>
        </div>
        
        <h2 class="risk-title">Your Heart Risk Assessment</h2>
        
        <!-- Risk Percentage Display -->
        <div class="risk-percentage-container">
          <div 
            class="risk-circle" 
            :class="getRiskClass(results.risk_percentage)"
          >
            <span class="risk-number">{{ results.risk_percentage }}%</span>
          </div>
        </div>
        
        <!-- Risk Category Badge -->
        <div class="risk-category">
          <span 
            class="badge"
            :class="results.prediction === 1 ? 'badge-danger' : 'badge-success'"
          >
            {{ results.prediction === 1 ? '🔴 At Risk' : '🟢 Safe' }}
          </span>
          <h3 :class="results.prediction === 1 ? 'text-danger' : 'text-success'">
            {{ results.risk_category }}
          </h3>
        </div>
        
        <!-- Personalized Message -->
        <div 
          class="alert"
          :class="getAlertClass(results.risk_percentage)"
        >
          <p class="message-text">{{ results.message }}</p>
        </div>
        
        <!-- Model Confidence -->
        <div class="confidence-info">
          <small>Model Confidence: {{ (results.confidence * 100).toFixed(1) }}%</small>
        </div>
      </div>
    </div>

    <!-- Recommendations Card -->
    <div class="card recommendations-card">
      <div class="card-header">
        <h3>📋 Personalized Health Recommendations</h3>
        <p>Based on your assessment, here's what you can do:</p>
      </div>
      
      <ul class="recommendations-list">
        <li 
          v-for="(recommendation, index) in results.recommendations" 
          :key="index"
          class="recommendation-item"
        >
          <span class="recommendation-icon">
            <span v-if="recommendation.includes('URGENT')">🚨</span>
            <span v-else>💡</span>
          </span>
          <span class="recommendation-text">{{ recommendation }}</span>
        </li>
      </ul>
    </div>

    <!-- Health Tips Card -->
    <div class="card health-tips-card">
      <div class="card-header">
        <h3>💪 General Heart Health Tips</h3>
      </div>
      
      <div class="tips-grid grid grid-2">
        <div class="tip-item">
          <span class="tip-emoji">🏃‍♂️</span>
          <h4>Stay Active</h4>
          <p>Aim for 30 minutes of moderate exercise daily</p>
        </div>
        
        <div class="tip-item">
          <span class="tip-emoji">🥗</span>
          <h4>Eat Healthy</h4>
          <p>Focus on fruits, vegetables, and whole grains</p>
        </div>
        
        <div class="tip-item">
          <span class="tip-emoji">😴</span>
          <h4>Sleep Well</h4>
          <p>Get 7-9 hours of quality sleep each night</p>
        </div>
        
        <div class="tip-item">
          <span class="tip-emoji">🧘‍♀️</span>
          <h4>Manage Stress</h4>
          <p>Practice meditation or relaxation techniques</p>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="action-buttons text-center">
      <button @click="handleReset" class="btn btn-primary">
        ↺ Check Another Profile
      </button>
      <button @click="downloadReport" class="btn btn-secondary">
        📄 Download Report
      </button>
    </div>

    <!-- Disclaimer -->
    <div class="disclaimer-box">
      <p>
        <strong>⚠️ Medical Disclaimer:</strong> This tool provides risk estimates based on AI analysis 
        and is not a substitute for professional medical diagnosis. Please consult a qualified healthcare 
        provider for accurate diagnosis and treatment recommendations.
      </p>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'ResultsDisplay',
  props: {
    results: {
      type: Object,
      required: true
    }
  },
  emits: ['reset'],
  setup(props, { emit }) {
    const getRiskClass = (percentage) => {
      if (percentage < 20) return 'risk-low'
      if (percentage < 50) return 'risk-medium'
      return 'risk-high'
    }

    const getAlertClass = (percentage) => {
      if (percentage < 20) return 'alert-success'
      if (percentage < 50) return 'alert-warning'
      return 'alert-danger'
    }

    const handleReset = () => {
      emit('reset')
    }

    const downloadReport = () => {
      // Create a simple text report
      const report = `
HeartCare AI - Cardiac Arrest Risk Assessment Report
Generated: ${new Date().toLocaleDateString()}

RESULTS:
--------
Risk Percentage: ${props.results.risk_percentage}%
Risk Category: ${props.results.risk_category}
Status: ${props.results.prediction === 1 ? 'At Risk' : 'Safe'}
Model Confidence: ${(props.results.confidence * 100).toFixed(1)}%

ASSESSMENT:
-----------
${props.results.message}

RECOMMENDATIONS:
----------------
${props.results.recommendations.map((rec, i) => `${i + 1}. ${rec}`).join('\n')}

DISCLAIMER:
-----------
This tool provides risk estimates based on AI analysis and is not a substitute 
for professional medical diagnosis. Please consult a qualified healthcare provider 
for accurate diagnosis and treatment recommendations.

---
HeartCare AI © 2025
      `.trim()

      // Download as text file
      const blob = new Blob([report], { type: 'text/plain' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `HeartCare-AI-Report-${new Date().toISOString().split('T')[0]}.txt`
      link.click()
      URL.revokeObjectURL(url)
    }

    return {
      getRiskClass,
      getAlertClass,
      handleReset,
      downloadReport
    }
  }
}
</script>

<style scoped>
.results-display {
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from { 
    opacity: 0; 
    transform: translateY(30px); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}

.result-card {
  background: linear-gradient(135deg, var(--white) 0%, var(--light-gray) 100%);
}

.risk-header {
  padding: var(--spacing-lg);
}

.risk-icon {
  font-size: 4rem;
  margin-bottom: var(--spacing-md);
  animation: bounce 1s ease-in-out;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.risk-title {
  color: var(--primary-dark);
  margin-bottom: var(--spacing-lg);
}

.risk-percentage-container {
  margin: var(--spacing-xl) 0;
  display: flex;
  justify-content: center;
}

.risk-circle {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-lg);
  position: relative;
  animation: scaleIn 0.6s ease-out;
}

@keyframes scaleIn {
  from { transform: scale(0); }
  to { transform: scale(1); }
}

.risk-low {
  background: linear-gradient(135deg, var(--success-green), #81c784);
  color: var(--white);
}

.risk-medium {
  background: linear-gradient(135deg, var(--warning-orange), #ffb74d);
  color: var(--white);
}

.risk-high {
  background: linear-gradient(135deg, var(--danger-red), #e57373);
  color: var(--white);
}

.risk-number {
  font-size: 3rem;
  font-weight: 700;
}

.risk-category {
  margin: var(--spacing-lg) 0;
}

.risk-category h3 {
  margin-top: var(--spacing-sm);
  font-size: var(--font-size-xl);
}

.message-text {
  font-size: var(--font-size-lg);
  font-weight: 500;
  margin: 0;
}

.confidence-info {
  margin-top: var(--spacing-md);
  color: var(--dark-gray);
}

/* Recommendations */
.recommendations-card {
  border-left: 4px solid var(--primary-blue);
}

.recommendations-list {
  list-style: none;
  padding: 0;
}

.recommendation-item {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
  background: var(--off-white);
  border-radius: var(--radius-md);
  transition: all 0.3s ease;
}

.recommendation-item:hover {
  background: var(--light-gray);
  transform: translateX(5px);
}

.recommendation-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.recommendation-text {
  flex: 1;
  line-height: 1.6;
}

/* Health Tips */
.health-tips-card {
  background: linear-gradient(135deg, var(--light-gray) 0%, var(--white) 100%);
}

.tips-grid {
  gap: var(--spacing-md);
}

.tip-item {
  text-align: center;
  padding: var(--spacing-md);
  background: var(--white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
}

.tip-item:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
}

.tip-emoji {
  font-size: 2.5rem;
  display: block;
  margin-bottom: var(--spacing-sm);
}

.tip-item h4 {
  color: var(--primary-blue);
  margin-bottom: var(--spacing-xs);
  font-size: var(--font-size-lg);
}

.tip-item p {
  color: var(--dark-gray);
  margin: 0;
  font-size: var(--font-size-sm);
}

/* Action Buttons */
.action-buttons {
  margin: var(--spacing-xl) 0;
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}

.action-buttons .btn {
  min-width: 200px;
}

/* Disclaimer */
.disclaimer-box {
  background: #fff8e1;
  border: 2px solid var(--warning-orange);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  margin-top: var(--spacing-lg);
}

.disclaimer-box p {
  margin: 0;
  font-size: var(--font-size-sm);
  color: var(--text-dark);
  line-height: 1.6;
}

/* Responsive */
@media (max-width: 768px) {
  .risk-circle {
    width: 150px;
    height: 150px;
  }
  
  .risk-number {
    font-size: 2rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .action-buttons .btn {
    width: 100%;
  }
  
  .tips-grid {
    grid-template-columns: 1fr;
  }
}
</style>
