<script setup>
import { ref, onMounted } from 'vue'
import { apiService } from './services/api.js'
import CategoriesList from './components/CategoriesList.vue'
import ProductsManager from './components/ProductsManager.vue'

// Estados reactivos
const isConnected = ref(false)
const connectionStatus = ref('Verificando conexión...')
const currentView = ref('home') // 'home', 'categories', 'products'
const mobileMenuOpen = ref(false)

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

// Mobile menu
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

// Navegación
const showCategories = () => {
  currentView.value = 'categories'
  closeMobileMenu()
}

const showProducts = () => {
  currentView.value = 'products'
  closeMobileMenu()
}

const showHome = () => {
  currentView.value = 'home'
  closeMobileMenu()
}

// Ejecutar al montar el componente
onMounted(async () => {
  await checkConnection()
})
</script>
<template>
  <div id="app">
    <!-- Header -->
    <header class="header">
      <div class="container">
        <div class="header-content">
          <div class="logo">
            <div class="logo-icon">🌱</div>
            <div class="logo-text">
              <h1>DulProMax</h1>
              <span class="tagline">Productos Saludables B2B</span>
            </div>
          </div>
          
          <!-- Mobile menu button -->
          <button class="mobile-menu-btn" @click="toggleMobileMenu">
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
        
        <nav class="nav" :class="{ 'nav-open': mobileMenuOpen }">
          <button 
            @click="showHome" 
            :class="{ 'active': currentView === 'home' }"
            class="nav-btn"
          >
            <span class="nav-icon">🏠</span>
            <span class="nav-text">Inicio</span>
          </button>
          <button 
            @click="showCategories" 
            :class="{ 'active': currentView === 'categories' }"
            class="nav-btn"
          >
            <span class="nav-icon">🏷️</span>
            <span class="nav-text">Categorías</span>
          </button>
          <button 
            @click="showProducts" 
            :class="{ 'active': currentView === 'products' }"
            class="nav-btn"
          >
            <span class="nav-icon">📦</span>
            <span class="nav-text">Productos</span>
          </button>
        </nav>
      </div>
    </header>

    <!-- Connection Status Banner -->
    <div v-if="!isConnected" class="connection-banner">
      <div class="container">
        <div class="connection-content">
          <div class="connection-icon">⚠️</div>
          <div class="connection-text">
            <h3>Verificando conexión...</h3>
            <p>{{ connectionStatus }}</p>
          </div>
        </div>
      </div>
    </div>

    <main class="main-content">
      <!-- Vista Home -->
      <div v-if="currentView === 'home'" class="home-view">
        <!-- Hero Section -->
        <section class="hero-section">
          <div class="container">
            <div class="hero-content">
              <div class="hero-text">
                <h1 class="hero-title">Plataforma B2B de Productos Saludables</h1>
                <p class="hero-subtitle">Gestiona tu catálogo, optimiza tus ventas y haz crecer tu negocio con nuestra solución integral para distribuidores de alimentos saludables.</p>
                <div class="hero-actions">
                  <button class="btn-primary" @click="showProducts">
                    <span class="btn-icon">📦</span>
                    Explorar Productos
                  </button>
                  <button class="btn-secondary" @click="showCategories">
                    <span class="btn-icon">🏷️</span>
                    Ver Categorías
                  </button>
                </div>
              </div>
              <div class="hero-visual">
                <div class="hero-card">
                  <div class="card-icon">🌱</div>
                  <h3>Productos Naturales</h3>
                  <p>Barras, granolas, panes integrales y dulces dietéticos</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Features Section -->
        <section class="features-section">
          <div class="container">
            <div class="section-header">
              <h2>Gestiona tu negocio de forma integral</h2>
              <p>Herramientas diseñadas específicamente para distribuidores B2B</p>
            </div>
            
            <div class="features-grid">
              <div class="feature-card clickable" @click="showCategories">
                <div class="feature-icon">🏷️</div>
                <h3>Gestión de Categorías</h3>
                <p>Organiza y administra las categorías de tus productos de manera eficiente</p>
                <div class="feature-status available">Disponible</div>
              </div>
              
              <div class="feature-card clickable" @click="showProducts">
                <div class="feature-icon">📦</div>
                <h3>Catálogo de Productos</h3>
                <p>CRUD completo para gestionar tu inventario con filtros y búsqueda avanzada</p>
                <div class="feature-status available">Disponible</div>
              </div>
              
              <div class="feature-card">
                <div class="feature-icon">🛒</div>
                <h3>Sistema de Pedidos</h3>
                <p>Plataforma optimizada para pedidos B2B con gestión de clientes</p>
                <div class="feature-status coming-soon">Próximamente</div>
              </div>
              
              <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3>Analytics y Reportes</h3>
                <p>Métricas de ventas, inventario y análisis de rendimiento</p>
                <div class="feature-status coming-soon">Próximamente</div>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- Vista Categorías -->
      <div v-else-if="currentView === 'categories'">
        <CategoriesList />
      </div>

      <!-- Vista Productos -->
      <div v-else-if="currentView === 'products'">
        <ProductsManager />
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
    </main>

    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-brand">
            <div class="footer-logo">
              <span class="logo-icon">🌱</span>
              <span class="logo-text">DulProMax</span>
            </div>
            <p class="footer-tagline">Productos Saludables B2B</p>
          </div>
          <div class="footer-info">
            <p>&copy; 2024 DulProMax. Todos los derechos reservados.</p>
            <p class="version-info">Versión 1.0.0 - Plataforma B2B</p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* Reset y base */
* {
  box-sizing: border-box;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: #1a202c;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* Header */
.header {
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  font-size: 2rem;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}

.logo-text h1 {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.tagline {
  font-size: 0.875rem;
  color: #6b7280;
  margin: 0;
  font-weight: 500;
}

/* Mobile menu button */
.mobile-menu-btn {
  display: none;
  flex-direction: column;
  gap: 4px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.mobile-menu-btn span {
  width: 24px;
  height: 2px;
  background: #374151;
  border-radius: 1px;
  transition: all 0.3s ease;
}

/* Navigation */
.nav {
  display: flex;
  gap: 0.5rem;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: transparent;
  border: none;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  transition: all 0.2s ease;
  text-decoration: none;
}

.nav-btn:hover {
  background: #f3f4f6;
  color: #059669;
}

.nav-btn.active {
  background: #ecfdf5;
  color: #059669;
  font-weight: 600;
}

.nav-icon {
  font-size: 1.125rem;
}

/* Connection Banner */
.connection-banner {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: white;
  padding: 1rem 0;
}

.connection-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  justify-content: center;
}

.connection-icon {
  font-size: 1.5rem;
}

.connection-text h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.connection-text p {
  margin: 0;
  font-size: 0.875rem;
  opacity: 0.9;
}

/* Main Content */
.main-content {
  flex: 1;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
  padding: 4rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1.1;
  margin: 0 0 1.5rem 0;
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #6b7280;
  margin: 0 0 2rem 0;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-primary, .btn-secondary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  text-decoration: none;
}

.btn-primary {
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(5, 150, 105, 0.4);
}

.btn-secondary {
  background: white;
  color: #059669;
  border: 2px solid #059669;
}

.btn-secondary:hover {
  background: #059669;
  color: white;
}

.btn-icon {
  font-size: 1.125rem;
}

/* Hero Visual */
.hero-visual {
  display: flex;
  justify-content: center;
}

.hero-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 300px;
  border: 1px solid #e5e7eb;
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.hero-card h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  color: #1f2937;
}

.hero-card p {
  color: #6b7280;
  margin: 0;
  font-size: 0.875rem;
}

/* Features Section */
.features-section {
  padding: 4rem 0;
  background: white;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-header h2 {
  font-weight: 700;
  margin: 0 0 1rem 0;
  color: #1f2937;
}

.section-header p {
  font-size: 1.125rem;
  color: #6b7280;
  margin: 0;
  max-width: 600px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
  position: relative;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-color: #10b981;
}

.feature-card.clickable {
  cursor: pointer;
}

.feature-card.clickable:hover {
  border-color: #059669;
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  display: block;
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 0.75rem 0;
  color: #1f2937;
}

.feature-card p {
  color: #6b7280;
  margin: 0 0 1.5rem 0;
  line-height: 1.6;
}

.feature-status {
  display: inline-block;
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.feature-status.available {
  background: #d1fae5;
  color: #065f46;
}

.feature-status.coming-soon {
  background: #fef3c7;
  color: #92400e;
}

/* Footer */
.footer {
  background: #1f2937;
  color: white;
  padding: 2rem 0;
  margin-top: auto;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.footer-logo .logo-icon {
  font-size: 1.5rem;
}

.footer-logo .logo-text {
  font-size: 1.25rem;
  font-weight: 700;
}

.footer-tagline {
  font-size: 0.875rem;
  color: #9ca3af;
  margin: 0;
}

.footer-info {
  text-align: right;
}

.footer-info p {
  margin: 0;
  font-size: 0.875rem;
  color: #9ca3af;
}

.version-info {
  opacity: 0.7;
}

/* Responsive Design */
@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .mobile-menu-btn {
    display: flex;
  }

  .nav {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border-top: 1px solid #e5e7eb;
    flex-direction: column;
    padding: 1rem;
    gap: 0;
  }

  .nav.nav-open {
    display: flex;
  }

  .nav-btn {
    justify-content: flex-start;
    padding: 1rem;
    border-radius: 0.5rem;
  }

  .hero-content {
    grid-template-columns: 1fr;
    gap: 2rem;
    text-align: center;
  }

  .hero-title {
    font-size: 2.25rem;
  }

  .hero-subtitle {
    font-size: 1.125rem;
  }

  .hero-actions {
    justify-content: center;
  }

  .btn-primary, .btn-secondary {
    width: 100%;
    justify-content: center;
  }

  .section-header h2 {
    font-size: 2rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .footer-content {
    flex-direction: column;
    text-align: center;
  }

  .footer-info {
    text-align: center;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 2rem 0;
  }

  .hero-title {
    font-size: 1.875rem;
  }

  .features-section {
    padding: 2rem 0;
  }

  .feature-card {
    padding: 1.5rem;
  }
}
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
