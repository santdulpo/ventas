<template>
  <div class="connection-test">
    <h3>🔧 Prueba de Conexión API</h3>
    
    <div class="test-buttons">
      <button @click="testEndpoint('/')" :disabled="loading">
        Probar Endpoint Principal
      </button>
      <button @click="testEndpoint('/ping')" :disabled="loading">
        Probar Ping
      </button>
      <button @click="testEndpoint('/health')" :disabled="loading">
        Probar Health Check
      </button>
      <button @click="testEndpoint('/api/productos')" :disabled="loading">
        Probar Productos
      </button>
    </div>

    <div v-if="loading" class="loading">
      ⏳ Probando conexión...
    </div>

    <div v-if="result" class="result" :class="{ 'success': result.success, 'error': !result.success }">
      <h4>{{ result.success ? '✅ Éxito' : '❌ Error' }}</h4>
      <p><strong>Endpoint:</strong> {{ result.endpoint }}</p>
      <p><strong>Status:</strong> {{ result.status }}</p>
      <div v-if="result.data" class="result-data">
        <p><strong>Respuesta:</strong></p>
        <pre>{{ JSON.stringify(result.data, null, 2) }}</pre>
      </div>
      <div v-if="result.error" class="result-error">
        <p><strong>Error:</strong> {{ result.error }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import apiService from '../services/api.js'

const loading = ref(false)
const result = ref(null)

async function testEndpoint(endpoint) {
  loading.value = true
  result.value = null
  
  try {
    const response = await apiService.request(endpoint)
    result.value = {
      success: true,
      endpoint: endpoint,
      status: 'OK',
      data: response
    }
  } catch (error) {
    result.value = {
      success: false,
      endpoint: endpoint,
      status: 'ERROR',
      error: error.message
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.connection-test {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin: 2rem 0;
}

.connection-test h3 {
  color: #333;
  margin-bottom: 1.5rem;
}

.test-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
}

.test-buttons button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 5px;
  background-color: #667eea;
  color: white;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.test-buttons button:hover:not(:disabled) {
  background-color: #5a67d8;
}

.test-buttons button:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  color: #666;
  font-style: italic;
}

.result {
  padding: 1rem;
  border-radius: 5px;
  margin-top: 1rem;
}

.result.success {
  background-color: #f0fff4;
  border: 1px solid #68d391;
}

.result.error {
  background-color: #fff5f5;
  border: 1px solid #fc8181;
}

.result h4 {
  margin: 0 0 0.5rem 0;
}

.result p {
  margin: 0.25rem 0;
}

.result-data,
.result-error {
  margin-top: 1rem;
}

.result-data pre {
  background-color: #f7fafc;
  padding: 1rem;
  border-radius: 5px;
  overflow-x: auto;
  font-size: 0.875rem;
}
</style>