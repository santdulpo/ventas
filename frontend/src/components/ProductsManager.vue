<template>
  <div class="products-manager">
    <div class="manager-header">
      <h2>🛍️ Gestión de Productos</h2>
      <button @click="showCreateForm" class="btn-primary">
        ➕ Nuevo Producto
      </button>
    </div>

    <!-- Filtros -->
    <div class="filters-section">
      <div class="filters-row">
        <input
          v-model="filters.search"
          @input="debouncedSearch"
          placeholder="🔍 Buscar productos..."
          class="search-input"
        />
        
        <select v-model="filters.category_id" @change="applyFilters" class="filter-select">
          <option value="">Todas las categorías</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>

        <select v-model="filters.active_only" @change="applyFilters" class="filter-select">
          <option :value="true">Solo activos</option>
          <option :value="false">Todos</option>
        </select>

        <button @click="clearFilters" class="btn-secondary">
          🗑️ Limpiar
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Cargando productos...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h3>Error al cargar productos</h3>
      <p>{{ error }}</p>
      <button @click="fetchProducts" class="retry-btn">
        🔄 Reintentar
      </button>
    </div>

    <!-- Products Table -->
    <div v-else-if="products.length > 0" class="products-table-container">
      <table class="products-table">
        <thead>
          <tr>
            <th>Imagen</th>
            <th>Nombre</th>
            <th>SKU</th>
            <th>Categoría</th>
            <th>Precio Mayorista</th>
            <th>Stock</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id" class="product-row">
            <td>
              <div class="product-image">
                <img 
                  v-if="product.main_image_url" 
                  :src="product.main_image_url" 
                  :alt="product.name"
                  @error="handleImageError"
                />
                <div v-else class="image-placeholder">📦</div>
              </div>
            </td>
            <td>
              <div class="product-name">
                <strong>{{ product.name }}</strong>
                <small v-if="product.description">{{ truncateText(product.description, 50) }}</small>
              </div>
            </td>
            <td>
              <span class="sku">{{ product.sku || '-' }}</span>
            </td>
            <td>
              <span v-if="product.category" class="category-tag">
                {{ product.category.name }}
              </span>
              <span v-else class="no-category">Sin categoría</span>
            </td>
            <td>
              <span class="price">${{ formatPrice(product.price_wholesale) }}</span>
            </td>
            <td>
              <span 
                class="stock" 
                :class="{ 'low-stock': product.stock_quantity <= product.min_stock_alert }"
              >
                {{ product.stock_quantity }}
              </span>
            </td>
            <td>
              <span 
                class="status-badge" 
                :class="{ 'active': product.is_active, 'inactive': !product.is_active }"
              >
                {{ product.is_active ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td>
              <div class="actions">
                <button @click="editProduct(product)" class="btn-edit" title="Editar">
                  ✏️
                </button>
                <button @click="confirmDelete(product)" class="btn-delete" title="Eliminar">
                  🗑️
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Paginación -->
      <div v-if="pagination.total_pages > 1" class="pagination">
        <button 
          @click="changePage(pagination.page - 1)"
          :disabled="pagination.page <= 1"
          class="btn-pagination"
        >
          ← Anterior
        </button>
        
        <span class="page-info">
          Página {{ pagination.page }} de {{ pagination.total_pages }}
          ({{ pagination.total }} productos)
        </span>
        
        <button 
          @click="changePage(pagination.page + 1)"
          :disabled="pagination.page >= pagination.total_pages"
          class="btn-pagination"
        >
          Siguiente →
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="empty-icon">📦</div>
      <h3>No hay productos</h3>
      <p>Comienza creando tu primer producto.</p>
      <button @click="showCreateForm" class="btn-primary">
        ➕ Crear Producto
      </button>
    </div>

    <!-- Modal para Crear/Editar Producto -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingProduct ? '✏️ Editar Producto' : '➕ Nuevo Producto' }}</h3>
          <button @click="closeModal" class="close-btn">✕</button>
        </div>
        
        <form @submit.prevent="saveProduct" class="product-form">
          <div class="form-row">
            <div class="form-group">
              <label>Nombre *</label>
              <input 
                v-model="formData.name" 
                type="text" 
                required 
                placeholder="Nombre del producto"
              />
            </div>
            <div class="form-group">
              <label>SKU</label>
              <input 
                v-model="formData.sku" 
                type="text" 
                placeholder="Código único del producto"
              />
            </div>
          </div>

          <div class="form-group">
            <label>Descripción</label>
            <textarea 
              v-model="formData.description" 
              placeholder="Descripción del producto"
              rows="3"
            ></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Categoría</label>
              <select v-model="formData.category_id">
                <option value="">Seleccionar categoría</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>Slug</label>
              <input 
                v-model="formData.slug" 
                type="text" 
                placeholder="url-amigable-del-producto"
              />
            </div>
          </div>

          <!-- Precios -->
          <div class="form-section">
            <h4>💰 Precios</h4>
            <div class="form-row">
              <div class="form-group">
                <label>Precio Retail *</label>
                <input 
                  v-model.number="formData.price_retail" 
                  type="number" 
                  step="0.01" 
                  min="0" 
                  required
                />
              </div>
              <div class="form-group">
                <label>Precio Mayorista *</label>
                <input 
                  v-model.number="formData.price_wholesale" 
                  type="number" 
                  step="0.01" 
                  min="0" 
                  required
                />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Precio Gimnasios</label>
                <input 
                  v-model.number="formData.price_gym" 
                  type="number" 
                  step="0.01" 
                  min="0"
                />
              </div>
              <div class="form-group">
                <label>Precio Cafeterías</label>
                <input 
                  v-model.number="formData.price_cafeteria" 
                  type="number" 
                  step="0.01" 
                  min="0"
                />
              </div>
            </div>
          </div>

          <!-- Inventario -->
          <div class="form-section">
            <h4>📦 Inventario</h4>
            <div class="form-row">
              <div class="form-group">
                <label>Stock Actual</label>
                <input 
                  v-model.number="formData.stock_quantity" 
                  type="number" 
                  min="0"
                />
              </div>
              <div class="form-group">
                <label>Alerta Stock Mínimo</label>
                <input 
                  v-model.number="formData.min_stock_alert" 
                  type="number" 
                  min="0"
                />
              </div>
            </div>
          </div>

          <!-- Estado -->
          <div class="form-section">
            <div class="form-row">
              <div class="form-group checkbox-group">
                <label>
                  <input 
                    v-model="formData.is_active" 
                    type="checkbox"
                  />
                  Producto activo
                </label>
              </div>
              <div class="form-group checkbox-group">
                <label>
                  <input 
                    v-model="formData.is_featured" 
                    type="checkbox"
                  />
                  Producto destacado
                </label>
              </div>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" @click="closeModal" class="btn-secondary">
              Cancelar
            </button>
            <button type="submit" :disabled="saving" class="btn-primary">
              {{ saving ? 'Guardando...' : (editingProduct ? 'Actualizar' : 'Crear') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal de Confirmación de Eliminación -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal-content delete-modal" @click.stop>
        <div class="modal-header">
          <h3>🗑️ Confirmar Eliminación</h3>
        </div>
        <div class="modal-body">
          <p>¿Estás seguro de que quieres eliminar el producto:</p>
          <strong>{{ productToDelete?.name }}</strong>
          <p class="warning">Esta acción no se puede deshacer.</p>
        </div>
        <div class="form-actions">
          <button @click="showDeleteModal = false" class="btn-secondary">
            Cancelar
          </button>
          <button @click="deleteProduct" :disabled="deleting" class="btn-danger">
            {{ deleting ? 'Eliminando...' : 'Eliminar' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { apiService } from '../services/api.js'

// Estado reactivo
const products = ref([])
const categories = ref([])
const loading = ref(false)
const error = ref(null)
const showModal = ref(false)
const showDeleteModal = ref(false)
const editingProduct = ref(null)
const productToDelete = ref(null)
const saving = ref(false)
const deleting = ref(false)

// Filtros y paginación
const filters = ref({
  search: '',
  category_id: '',
  active_only: true,
  page: 1,
  per_page: 10
})

const pagination = ref({
  total: 0,
  page: 1,
  per_page: 10,
  total_pages: 1
})

// Formulario
const formData = ref({
  name: '',
  description: '',
  slug: '',
  sku: '',
  category_id: '',
  price_retail: 0,
  price_wholesale: 0,
  price_gym: null,
  price_cafeteria: null,
  stock_quantity: 0,
  min_stock_alert: 10,
  is_active: true,
  is_featured: false
})

// Métodos
const fetchProducts = async () => {
  loading.value = true
  error.value = null
  
  try {
    console.log('🔄 Cargando productos...')
    const data = await apiService.getProducts(filters.value)
    products.value = data.products
    pagination.value = {
      total: data.total,
      page: data.page,
      per_page: data.per_page,
      total_pages: data.total_pages
    }
    console.log('✅ Productos cargados:', data.products.length)
  } catch (err) {
    console.error('❌ Error al cargar productos:', err)
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const data = await apiService.getCategories()
    categories.value = data
  } catch (err) {
    console.error('Error al cargar categorías:', err)
  }
}

const applyFilters = () => {
  filters.value.page = 1
  fetchProducts()
}

const debouncedSearch = (() => {
  let timeout
  return () => {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      applyFilters()
    }, 500)
  }
})()

const clearFilters = () => {
  filters.value = {
    search: '',
    category_id: '',
    active_only: true,
    page: 1,
    per_page: 10
  }
  fetchProducts()
}

const changePage = (newPage) => {
  filters.value.page = newPage
  fetchProducts()
}

const showCreateForm = () => {
  editingProduct.value = null
  resetForm()
  showModal.value = true
}

const editProduct = (product) => {
  editingProduct.value = product
  formData.value = { ...product }
  if (product.category) {
    formData.value.category_id = product.category.id
  }
  showModal.value = true
}

const resetForm = () => {
  formData.value = {
    name: '',
    description: '',
    slug: '',
    sku: '',
    category_id: '',
    price_retail: 0,
    price_wholesale: 0,
    price_gym: null,
    price_cafeteria: null,
    stock_quantity: 0,
    min_stock_alert: 10,
    is_active: true,
    is_featured: false
  }
}

const closeModal = () => {
  showModal.value = false
  editingProduct.value = null
  resetForm()
}

const saveProduct = async () => {
  saving.value = true
  
  try {
    if (editingProduct.value) {
      await apiService.updateProduct(editingProduct.value.id, formData.value)
    } else {
      await apiService.createProduct(formData.value)
    }
    
    closeModal()
    fetchProducts()
  } catch (err) {
    alert(`Error: ${err.message}`)
  } finally {
    saving.value = false
  }
}

const confirmDelete = (product) => {
  productToDelete.value = product
  showDeleteModal.value = true
}

const deleteProduct = async () => {
  deleting.value = true
  
  try {
    await apiService.deleteProduct(productToDelete.value.id)
    showDeleteModal.value = false
    productToDelete.value = null
    fetchProducts()
  } catch (err) {
    alert(`Error: ${err.message}`)
  } finally {
    deleting.value = false
  }
}

// Utilidades
const formatPrice = (price) => {
  return new Intl.NumberFormat('es-CO', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2
  }).format(price)
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

const handleImageError = (event) => {
  event.target.style.display = 'none'
}

// Cargar datos al montar
onMounted(() => {
  fetchCategories()
  fetchProducts()
})
</script>

<style scoped>
.products-manager {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.manager-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.manager-header h2 {
  color: #2c3e50;
  margin: 0;
}

/* Filtros */
.filters-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.filters-row {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 250px;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.filter-select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  min-width: 150px;
}

/* Botones */
.btn-primary {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background: #2980b9;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.btn-secondary:hover {
  background: #7f8c8d;
}

.btn-danger {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.btn-danger:hover {
  background: #c0392b;
}

/* Estados de carga */
.loading-state, .error-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 3rem;
  text-align: center;
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

.error-state {
  color: #e74c3c;
}

.retry-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 1rem;
}

/* Tabla */
.products-table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.products-table {
  width: 100%;
  border-collapse: collapse;
}

.products-table th {
  background: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 1px solid #dee2e6;
}

.products-table td {
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
  vertical-align: middle;
}

.product-row:hover {
  background: #f8f9fa;
}

.product-image {
  width: 50px;
  height: 50px;
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  font-size: 1.5rem;
  color: #7f8c8d;
}

.product-name strong {
  display: block;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.product-name small {
  color: #7f8c8d;
  font-size: 0.85rem;
}

.sku {
  font-family: monospace;
  background: #f8f9fa;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
}

.category-tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.85rem;
}

.no-category {
  color: #7f8c8d;
  font-style: italic;
}

.price {
  font-weight: 600;
  color: #27ae60;
}

.stock {
  font-weight: 600;
}

.stock.low-stock {
  color: #e74c3c;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status-badge.active {
  background: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background: #f8d7da;
  color: #721c24;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit, .btn-delete {
  background: none;
  border: none;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.btn-edit:hover {
  background: #e3f2fd;
}

.btn-delete:hover {
  background: #ffebee;
}

/* Paginación */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-top: 1px solid #dee2e6;
}

.btn-pagination {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn-pagination:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.page-info {
  color: #7f8c8d;
}

/* Modal */
.modal-overlay {
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

.modal-content {
  background: white;
  border-radius: 8px;
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #dee2e6;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
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

/* Formulario */
.product-form {
  padding: 1.5rem;
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  flex: 1;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.form-section {
  margin: 2rem 0;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 6px;
}

.form-section h4 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.checkbox-group input[type="checkbox"] {
  width: auto;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #dee2e6;
}

.delete-modal {
  max-width: 400px;
}

.modal-body {
  padding: 1.5rem;
}

.warning {
  color: #e74c3c;
  font-size: 0.9rem;
  margin-top: 1rem;
}

/* Responsive */
@media (max-width: 768px) {
  .products-manager {
    padding: 1rem;
  }
  
  .manager-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .filters-row {
    flex-direction: column;
  }
  
  .search-input,
  .filter-select {
    min-width: auto;
  }
  
  .products-table-container {
    overflow-x: auto;
  }
  
  .products-table {
    min-width: 800px;
  }
  
  .form-row {
    flex-direction: column;
  }
  
  .modal-content {
    width: 95%;
    margin: 1rem;
  }
}
</style>
