// Servicio API para DulProMax
import axios from 'axios'

// Configuración base de la API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://ventas-bfzl.onrender.com'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor para manejo de errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// Servicios de la API
export const apiService = {
  // Test de conexión
  async testConnection() {
    try {
      const response = await api.get('/health')
      return response.data
    } catch (error) {
      throw new Error(`Error de conexión: ${error.message}`)
    }
  },

  // === CATEGORÍAS ===
  async getCategories(activeOnly = true) {
    try {
      const response = await api.get('/api/v1/categories/', {
        params: { active_only: activeOnly }
      })
      return response.data
    } catch (error) {
      throw new Error(`Error al obtener categorías: ${error.message}`)
    }
  },

  async getCategory(categoryId) {
    try {
      const response = await api.get(`/api/v1/categories/${categoryId}/`)
      return response.data
    } catch (error) {
      throw new Error(`Error al obtener categoría: ${error.message}`)
    }
  },

  async createCategory(categoryData) {
    try {
      const response = await api.post('/api/v1/categories/', categoryData)
      return response.data
    } catch (error) {
      throw new Error(`Error al crear categoría: ${error.message}`)
    }
  },

  async updateCategory(categoryId, categoryData) {
    try {
      const response = await api.put(`/api/v1/categories/${categoryId}/`, categoryData)
      return response.data
    } catch (error) {
      throw new Error(`Error al actualizar categoría: ${error.message}`)
    }
  },

  async deleteCategory(categoryId) {
    try {
      await api.delete(`/api/v1/categories/${categoryId}/`)
      return true
    } catch (error) {
      throw new Error(`Error al eliminar categoría: ${error.message}`)
    }
  },

  // === PRODUCTOS ===
  async getProducts(params = {}) {
    try {
      const response = await api.get('/api/v1/products/', { params })
      return response.data
    } catch (error) {
      throw new Error(`Error al obtener productos: ${error.message}`)
    }
  },

  async getProduct(productId) {
    try {
      const response = await api.get(`/api/v1/products/${productId}/`)
      return response.data
    } catch (error) {
      throw new Error(`Error al obtener producto: ${error.message}`)
    }
  },

  async createProduct(productData) {
    try {
      const response = await api.post('/api/v1/products/', productData)
      return response.data
    } catch (error) {
      throw new Error(`Error al crear producto: ${error.message}`)
    }
  },

  async updateProduct(productId, productData) {
    try {
      const response = await api.put(`/api/v1/products/${productId}/`, productData)
      return response.data
    } catch (error) {
      throw new Error(`Error al actualizar producto: ${error.message}`)
    }
  },

  async deleteProduct(productId) {
    try {
      await api.delete(`/api/v1/products/${productId}/`)
      return true
    } catch (error) {
      throw new Error(`Error al eliminar producto: ${error.message}`)
    }
  }
}

export default apiService