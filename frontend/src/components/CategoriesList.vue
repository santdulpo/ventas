<template>
  <div class="categories-container">
    <div class="categories-header">
      <h2>🏷️ Categorías de Productos</h2>
      <p>Explora nuestro catálogo organizado por categorías</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Cargando categorías...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h3>Error al cargar categorías</h3>
      <p>{{ error }}</p>
      <button @click="fetchCategories" class="retry-btn">
        🔄 Reintentar
      </button>
    </div>

    <!-- Categories Grid -->
    <div v-else-if="categories.length > 0" class="categories-grid">
      <div 
        v-for="category in categories" 
        :key="category.id"
        class="category-card"
        @click="selectCategory(category)"
      >
        <div class="category-image">
          <img 
            v-if="category.image_url" 
            :src="category.image_url" 
            :alt="category.name"
            @error="handleImageError"
          />
          <div v-else class="category-placeholder">
            📦
          </div>
        </div>
        
        <div class="category-info">
          <h3>{{ category.name }}</h3>
          <p v-if="category.description">{{ category.description }}</p>
          <div class="category-meta">
            <span class="category-slug">#{{ category.slug }}</span>
            <span v-if="category.is_active" class="status-active">Activa</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="empty-icon">📋</div>
      <h3>No hay categorías disponibles</h3>
      <p>Aún no se han configurado categorías de productos.</p>
    </div>

    <!-- Selected Category Details -->
    <div v-if="selectedCategory" class="category-details">
      <div class="details-header">
        <h3>{{ selectedCategory.name }}</h3>
        <button @click="selectedCategory = null" class="close-btn">✕</button>
      </div>
      <div class="details-content">
        <p><strong>Descripción:</strong> {{ selectedCategory.description || 'Sin descripción' }}</p>
        <p><strong>Slug:</strong> {{ selectedCategory.slug }}</p>
        <p><strong>Estado:</strong> {{ selectedCategory.is_active ? 'Activa' : 'Inactiva' }}</p>
        <p><strong>Creada:</strong> {{ formatDate(selectedCategory.created_at) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { apiService } from '../services/api.js'

// Estado reactivo
const categories = ref([])
const loading = ref(false)
const error = ref(null)
const selectedCategory = ref(null)

// Métodos
const fetchCategories = async () => {
  loading.value = true
  error.value = null
  
  try {
    console.log('🔄 Cargando categorías...')
    const data = await apiService.getCategories()
    categories.value = data
    console.log('✅ Categorías cargadas:', data.length)
  } catch (err) {
    console.error('❌ Error al cargar categorías:', err)
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const selectCategory = (category) => {
  selectedCategory.value = category
}

const handleImageError = (event) => {
  event.target.style.display = 'none'
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Cargar categorías al montar el componente
onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.categories-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.categories-header {
  text-align: center;
  margin-bottom: 2rem;
}

.categories-header h2 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 2rem;
}

.categories-header p {
  color: #7f8c8d;
  font-size: 1.1rem;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 3rem;
  color: #7f8c8d;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #ecf0f1;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Error State */
.error-state {
  text-align: center;
  padding: 3rem;
  color: #e74c3c;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.retry-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  margin-top: 1rem;
  transition: background-color 0.3s;
}

.retry-btn:hover {
  background: #2980b9;
}

/* Categories Grid */
.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.category-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.category-image {
  height: 150px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.category-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.category-placeholder {
  font-size: 3rem;
  color: white;
}

.category-info {
  padding: 1.5rem;
}

.category-info h3 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 1.3rem;
}

.category-info p {
  color: #7f8c8d;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.category-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category-slug {
  background: #ecf0f1;
  color: #7f8c8d;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
}

.status-active {
  background: #2ecc71;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #7f8c8d;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

/* Category Details Modal */
.category-details {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.category-details > div {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.details-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  border-bottom: 1px solid #ecf0f1;
  padding-bottom: 1rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #7f8c8d;
}

.close-btn:hover {
  color: #e74c3c;
}

.details-content p {
  margin-bottom: 0.75rem;
  line-height: 1.6;
}

/* Responsive */
@media (max-width: 768px) {
  .categories-container {
    padding: 1rem;
  }
  
  .categories-grid {
    grid-template-columns: 1fr;
  }
  
  .categories-header h2 {
    font-size: 1.5rem;
  }
}
</style>
