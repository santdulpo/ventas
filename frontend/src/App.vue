<script setup>
import { ref, onMounted } from 'vue'
import apiService from './services/api.js'
import ConnectionTest from './components/ConnectionTest.vue'

// Estados reactivos
const isConnected = ref(false)
const connectionStatus = ref('Conectando...')
const backendData = ref(null)
const productos = ref([])
const stats = ref(null)
const loading = ref(true)

// Función para verificar conexión con el backend
async function checkConnection() {
  try {
    const response = await apiService.getHealth()
    if (response.status === 'healthy') {
      isConnected.value = true
      connectionStatus.value = '✅ Conectado al Backend'
      backendData.value = response
    }
  } catch (error) {
    isConnected.value = false
    connectionStatus.value = '❌ Error de conexión'
    console.error('Error connecting to backend:', error)
  }
}

// Función para cargar datos de ejemplo
async function loadData() {
  try {
    // Cargar productos
    const productosData = await apiService.getProductos()
    productos.value = productosData.productos

    // Cargar estadísticas
    const statsData = await apiService.getStats()
    stats.value = statsData

  } catch (error) {
    console.error('Error loading data:', error)
  } finally {
    loading.value = false
  }
}

// Ejecutar al montar el componente
onMounted(async () => {
  await checkConnection()
  if (isConnected.value) {
    await loadData()
  } else {
    loading.value = false
  }
})
</script>

<template>
  <div id="app">
    <header class="app-header">
      <div class="container">
        <h1 class="logo">🥗 DulProMax</h1>
        <p class="tagline">Plataforma B2B de Alimentos Saludables</p>
        
        <!-- Indicador de conexión -->
        <div class="connection-status" :class="{ 'connected': isConnected, 'disconnected': !isConnected }">
          {{ connectionStatus }}
        </div>
    </div>
  </header>

    <main class="app-main">
      <div class="container">
        <div class="welcome-section">
          <h2>¡Bienvenido a DulProMax!</h2>
          <p>Tu socio tecnológico para el crecimiento de tu negocio de alimentos saludables.</p>
          
          <!-- Estadísticas del Dashboard -->
          <div v-if="isConnected && stats" class="stats-grid">
            <div class="stat-card">
              <h3>💰 Ventas del Mes</h3>
              <p class="stat-number">${{ stats.ventas_mes.toLocaleString() }}</p>
            </div>
            <div class="stat-card">
              <h3>📦 Productos Activos</h3>
              <p class="stat-number">{{ stats.productos_activos }}</p>
            </div>
            <div class="stat-card">
              <h3>👥 Clientes</h3>
              <p class="stat-number">{{ stats.clientes_registrados }}</p>
            </div>
            <div class="stat-card">
              <h3>📋 Pedidos Pendientes</h3>
              <p class="stat-number">{{ stats.pedidos_pendientes }}</p>
            </div>
          </div>

          <!-- Productos de ejemplo -->
          <div v-if="isConnected && productos.length > 0" class="productos-section">
            <h3>🛒 Productos Destacados</h3>
            <div class="productos-grid">
              <div v-for="producto in productos" :key="producto.id" class="producto-card">
                <h4>{{ producto.nombre }}</h4>
                <p class="precio">${{ producto.precio }}</p>
                <span class="categoria">{{ producto.categoria }}</span>
              </div>
            </div>
          </div>
          
          <div class="features-grid">
            <div class="feature-card">
              <h3>🛒 E-commerce</h3>
              <p>Tienda online personalizada para tu negocio</p>
            </div>
            <div class="feature-card">
              <h3>📊 Gestión</h3>
              <p>Control de inventario y ventas en tiempo real</p>
            </div>
            <div class="feature-card">
              <h3>📱 Marketing</h3>
              <p>Herramientas digitales para fidelizar clientes</p>
            </div>
            <div class="feature-card">
              <h3>🚀 Crecimiento</h3>
              <p>Escala tu negocio con tecnología moderna</p>
            </div>
          </div>

          <!-- Loading state -->
          <div v-if="loading" class="loading">
            <p>⏳ Cargando datos...</p>
          </div>

          <!-- Componente de prueba de conexión (solo se muestra si hay problemas) -->
          <ConnectionTest v-if="!isConnected" />
        </div>
      </div>
  </main>

    <footer class="app-footer">
      <div class="container">
        <p>&copy; 2024 DulProMax. Todos los derechos reservados.</p>
        <p v-if="backendData" class="api-info">
          API: {{ backendData.service }} v{{ backendData.version }}
        </p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem 0;
  text-align: center;
}

.logo {
  font-size: 2.5rem;
  margin: 0;
  font-weight: bold;
}

.tagline {
  font-size: 1.2rem;
  margin: 0.5rem 0;
  opacity: 0.9;
}

.connection-status {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  display: inline-block;
}

.connection-status.connected {
  background-color: rgba(72, 187, 120, 0.2);
  border: 2px solid #48bb78;
}

.connection-status.disconnected {
  background-color: rgba(245, 101, 101, 0.2);
  border: 2px solid #f56565;
}

.app-main {
  flex: 1;
  padding: 3rem 0;
  background-color: #f8f9fa;
}

.welcome-section {
  text-align: center;
}

.welcome-section h2 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 1rem;
}

.welcome-section p {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 3rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #667eea;
}

.stat-card h3 {
  font-size: 1rem;
  color: #666;
  margin: 0 0 0.5rem 0;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.productos-section {
  margin: 3rem 0;
}

.productos-section h3 {
  color: #333;
  margin-bottom: 1.5rem;
}

.productos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.producto-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.producto-card:hover {
  transform: translateY(-3px);
}

.producto-card h4 {
  color: #333;
  margin: 0 0 0.5rem 0;
}

.precio {
  font-size: 1.5rem;
  font-weight: bold;
  color: #667eea;
  margin: 0.5rem 0;
}

.categoria {
  background-color: #f1f5f9;
  color: #64748b;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.875rem;
  text-transform: capitalize;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h3 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

.loading {
  font-size: 1.2rem;
  color: #666;
  margin: 2rem 0;
}

.app-footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 1.5rem 0;
}

.api-info {
  font-size: 0.875rem;
  opacity: 0.7;
  margin-top: 0.5rem;
}

@media (max-width: 768px) {
  .logo {
    font-size: 2rem;
  }
  
  .welcome-section h2 {
    font-size: 2rem;
  }
  
  .features-grid,
  .productos-grid,
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-number {
    font-size: 1.5rem;
  }
}
</style>
