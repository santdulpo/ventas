<script setup>
import { ref, onMounted } from 'vue'
import { apiService } from './services/api.js'
import CategoriesList from './components/CategoriesList.vue'

// Estados reactivos
const isConnected = ref(false)
const connectionStatus = ref('Verificando conexión...')
const currentView = ref('home') // 'home', 'categories'

// Función para verificar conexión con el backend
async function checkConnection() {
  try {
    const response = await apiService.testConnection()
    if (response.status === 'healthy') {
      isConnected.value = true
      connectionStatus.value = '✅ Conectado al Backend'
    }
  } catch (error) {
    isConnected.value = false
    connectionStatus.value = '❌ Error de conexión'
    console.error('Error connecting to backend:', error)
  }
}

// Navegación
const showCategories = () => {
  currentView.value = 'categories'
}

const showHome = () => {
  currentView.value = 'home'
}

// Ejecutar al montar el componente
onMounted(async () => {
  await checkConnection()
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

        <!-- Navegación -->
        <nav class="main-nav" v-if="isConnected">
          <button 
            @click="showHome" 
            :class="{ 'active': currentView === 'home' }"
            class="nav-btn"
          >
            🏠 Inicio
          </button>
          <button 
            @click="showCategories" 
            :class="{ 'active': currentView === 'categories' }"
            class="nav-btn"
          >
            🏷️ Categorías
          </button>
        </nav>
      </div>
    </header>

    <main class="app-main">
      <div class="container">
        <!-- Vista Home -->
        <div v-if="currentView === 'home'" class="home-view">
          <div class="welcome-section">
            <h2>¡Bienvenido a DulProMax!</h2>
            <p>Tu socio tecnológico para el crecimiento de tu negocio de alimentos saludables.</p>
            
            <div class="features-grid">
              <div class="feature-card" @click="showCategories">
                <h3>🏷️ Catálogo</h3>
                <p>Explora nuestras categorías de productos saludables</p>
                <span class="cta">Ver Categorías →</span>
              </div>
              <div class="feature-card">
                <h3>📊 Gestión</h3>
                <p>Control de inventario y ventas en tiempo real</p>
                <span class="coming-soon">Próximamente</span>
              </div>
              <div class="feature-card">
                <h3>📱 Pedidos</h3>
                <p>Sistema de pedidos B2B optimizado</p>
                <span class="coming-soon">Próximamente</span>
              </div>
              <div class="feature-card">
                <h3>🚀 Analytics</h3>
                <p>Reportes y análisis de ventas</p>
                <span class="coming-soon">Próximamente</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Vista Categorías -->
        <div v-else-if="currentView === 'categories'">
          <CategoriesList />
        </div>

        <!-- Error de conexión -->
        <div v-if="!isConnected" class="connection-error">
          <div class="error-content">
            <h2>⚠️ Error de Conexión</h2>
            <p>No se pudo conectar con el servidor. Por favor, verifica tu conexión e intenta nuevamente.</p>
            <button @click="checkConnection" class="retry-btn">
              🔄 Reintentar Conexión
            </button>
          </div>
        </div>
      </div>
    </main>

    <footer class="app-footer">
      <div class="container">
        <p>&copy; 2024 DulProMax. Todos los derechos reservados.</p>
        <p class="version-info">Versión 1.0.0 - Catálogo B2B</p>
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

/* Navegación */
.main-nav {
  margin-top: 1.5rem;
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.nav-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

.nav-btn.active {
  background: white;
  color: #667eea;
  border-color: white;
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
  cursor: pointer;
  position: relative;
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
  margin-bottom: 1rem;
}

.cta {
  color: #667eea;
  font-weight: bold;
  font-size: 0.9rem;
}

.coming-soon {
  background: #f1f5f9;
  color: #64748b;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  position: absolute;
  top: 1rem;
  right: 1rem;
}

.loading {
  font-size: 1.2rem;
  color: #666;
  margin: 2rem 0;
}

/* Error de conexión */
.connection-error {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.error-content {
  text-align: center;
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 500px;
}

.error-content h2 {
  color: #e74c3c;
  margin-bottom: 1rem;
}

.error-content p {
  color: #666;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.retry-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.retry-btn:hover {
  background: #2980b9;
}

.app-footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 1.5rem 0;
}

.version-info {
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
