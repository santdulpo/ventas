<template>
  <div class="categories-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="container">
        <div class="header-content">
          <div class="header-text">
            <h1 class="page-title">Gestión de Categorías</h1>
            <p class="page-subtitle">Organiza y administra las categorías de tus productos saludables</p>
          </div>
          <div class="header-actions">
            <button class="btn-primary" @click="showCreateModal = true">
              <span class="btn-icon">➕</span>
              Nueva Categoría
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <div class="container">

        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <div class="loading-content">
            <div class="spinner"></div>
            <h3>Cargando categorías...</h3>
            <p>Obteniendo la información más reciente</p>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="error-state">
          <div class="error-content">
            <div class="error-icon">⚠️</div>
            <h3>Error al cargar categorías</h3>
            <p>{{ error }}</p>
            <button @click="fetchCategories" class="btn-secondary">
              <span class="btn-icon">🔄</span>
              Reintentar
            </button>
          </div>
        </div>

        <!-- Categories Grid -->
        <div v-else-if="categories.length > 0" class="categories-section">
          <div class="section-header">
            <h2>Categorías Disponibles</h2>
            <p>{{ categories.length }} categoría{{ categories.length !== 1 ? 's' : '' }} registrada{{ categories.length !== 1 ? 's' : '' }}</p>
          </div>
          
          <div class="categories-grid">
            <div 
              v-for="category in categories" 
              :key="category.id"
              class="category-card"
            >
              <div class="card-header">
                <div class="category-icon">
                  <img 
                    v-if="category.image_url" 
                    :src="category.image_url" 
                    :alt="category.name"
                    @error="handleImageError"
                  />
                  <div v-else class="icon-placeholder">
                    🏷️
                  </div>
                </div>
                <div class="card-actions">
                  <button class="action-btn" @click="editCategory(category)" title="Editar">
                    ✏️
                  </button>
                  <button class="action-btn danger" @click="deleteCategory(category)" title="Eliminar">
                    🗑️
                  </button>
                </div>
              </div>
              
              <div class="card-content">
                <h3 class="category-name">{{ category.name }}</h3>
                <p class="category-description">{{ category.description || 'Sin descripción' }}</p>
                
                <div class="category-meta">
                  <span class="category-slug">
                    <span class="meta-label">Slug:</span>
                    {{ category.slug }}
                  </span>
                  <div class="category-status">
                    <span :class="['status-badge', category.is_active ? 'active' : 'inactive']">
                      {{ category.is_active ? 'Activa' : 'Inactiva' }}
                    </span>
                  </div>
                </div>
                
                <div class="category-footer">
                  <span class="created-date">
                    Creada: {{ formatDate(category.created_at) }}
                  </span>
                  <button class="btn-view" @click="selectCategory(category)">
                    Ver Detalles
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <div class="empty-content">
            <div class="empty-icon">🏷️</div>
            <h3>No hay categorías disponibles</h3>
            <p>Comienza creando tu primera categoría de productos</p>
            <button class="btn-primary" @click="showCreateModal = true">
              <span class="btn-icon">➕</span>
              Crear Primera Categoría
            </button>
          </div>
        </div>
      </div>
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
const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingCategory = ref(null)

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

const editCategory = (category) => {
  editingCategory.value = { ...category }
  showEditModal.value = true
}

const deleteCategory = async (category) => {
  if (confirm(`¿Estás seguro de que quieres eliminar la categoría "${category.name}"?`)) {
    try {
      await apiService.deleteCategory(category.id)
      await fetchCategories()
      console.log('✅ Categoría eliminada exitosamente')
    } catch (err) {
      console.error('❌ Error al eliminar categoría:', err)
      alert('Error al eliminar la categoría: ' + err.message)
    }
  }
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
/* Container */
.categories-page {
  min-height: 100vh;
  background: #f8fafc;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* Page Header */
.page-header {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 2rem 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.header-text {
  flex: 1;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  color: #1f2937;
}

.page-subtitle {
  font-size: 1.125rem;
  color: #6b7280;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

/* Buttons */
.btn-primary, .btn-secondary, .btn-view {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.875rem;
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

.btn-view {
  background: #f3f4f6;
  color: #374151;
  font-size: 0.75rem;
  padding: 0.5rem 0.75rem;
}

.btn-view:hover {
  background: #e5e7eb;
}

.btn-icon {
  font-size: 1rem;
}

/* Main Content */
.main-content {
  padding: 2rem 0;
}

/* Loading State */
.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.loading-content {
  text-align: center;
  color: #6b7280;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top: 4px solid #10b981;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-content h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.loading-content p {
  margin: 0;
  font-size: 0.875rem;
}

/* Error State */
.error-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.error-content {
  text-align: center;
  max-width: 400px;
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
}

.error-content h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #dc2626;
  margin: 0 0 1rem 0;
}

.error-content p {
  color: #6b7280;
  margin: 0 0 2rem 0;
  line-height: 1.6;
}

/* Empty State */
.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.empty-content {
  text-align: center;
  max-width: 400px;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  opacity: 0.5;
}

.empty-content h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #374151;
  margin: 0 0 1rem 0;
}

.empty-content p {
  color: #6b7280;
  margin: 0 0 2rem 0;
  line-height: 1.6;
}

/* Categories Section */
.categories-section {
  margin-top: 1rem;
}

.section-header {
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.section-header p {
  color: #6b7280;
  margin: 0;
  font-size: 0.875rem;
}

/* Categories Grid */
.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.category-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.category-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-color: #10b981;
}

/* Card Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 1.5rem 0;
}

.category-icon {
  width: 60px;
  height: 60px;
  border-radius: 0.75rem;
  background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #a7f3d0;
}

.category-icon img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0.75rem;
}

.icon-placeholder {
  font-size: 1.5rem;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 0.375rem;
  background: #f3f4f6;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: #e5e7eb;
}

.action-btn.danger:hover {
  background: #fecaca;
  color: #dc2626;
}

/* Card Content */
.card-content {
  padding: 1.5rem;
}

.category-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.category-description {
  color: #6b7280;
  margin: 0 0 1.5rem 0;
  line-height: 1.5;
  font-size: 0.875rem;
}

.category-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f3f4f6;
}

.category-slug {
  font-size: 0.75rem;
  color: #6b7280;
}

.meta-label {
  font-weight: 500;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-badge.active {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.inactive {
  background: #fee2e2;
  color: #991b1b;
}

.category-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.created-date {
  font-size: 0.75rem;
  color: #9ca3af;
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
  padding: 1rem;
}

.category-details > div {
  background: white;
  border-radius: 0.75rem;
  padding: 2rem;
  max-width: 500px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.1);
}

.details-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.details-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0.25rem;
  border-radius: 0.375rem;
  transition: all 0.2s ease;
}

.close-btn:hover {
  color: #dc2626;
  background: #fef2f2;
}

.details-content p {
  margin-bottom: 1rem;
  line-height: 1.6;
  color: #374151;
}

.details-content strong {
  color: #1f2937;
  font-weight: 600;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
  }

  .page-title {
    font-size: 2rem;
  }

  .categories-grid {
    grid-template-columns: 1fr;
  }

  .category-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .category-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 1rem;
  }

  .page-header {
    padding: 1.5rem 0;
  }

  .main-content {
    padding: 1.5rem 0;
  }

  .card-content {
    padding: 1rem;
  }
}
</style>
