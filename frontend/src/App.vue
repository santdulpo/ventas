<script setup>
// App principal para DulProMax B2B
</script>

<template>
  <div id="app">
    <header class="app-header">
      <div class="container">
        <h1 class="logo">🥗 DulProMax</h1>
        <p class="tagline">Plataforma B2B de Alimentos Saludables</p>
    </div>
  </header>

    <main class="app-main">
      <div class="container">
        <div class="welcome-section">
          <h2>¡Bienvenido a DulProMax!</h2>
          <p>Tu socio tecnológico para el crecimiento de tu negocio de alimentos saludables.</p>
          
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
        </div>
      </div>
  </main>

    <footer class="app-footer">
      <div class="container">
        <p>&copy; 2024 DulProMax. Todos los derechos reservados.</p>
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
  margin: 0.5rem 0 0 0;
  opacity: 0.9;
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

.app-footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 1.5rem 0;
}

@media (max-width: 768px) {
  .logo {
    font-size: 2rem;
  }
  
  .welcome-section h2 {
    font-size: 2rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
