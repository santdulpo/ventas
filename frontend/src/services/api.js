// Servicio API para DulProMax
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://ventas-bfzl.onrender.com'

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL
    console.log('🔗 API Service inicializado con URL:', this.baseURL)
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  }

  // Endpoints específicos
  async getWelcome() {
    return this.request('/')
  }

  async ping() {
    return this.request('/ping')
  }

  async getHealth() {
    return this.request('/health')
  }

  async getProductos() {
    return this.request('/api/productos')
  }

  async getStats() {
    return this.request('/api/stats')
  }
}

// Exportar instancia única
export const apiService = new ApiService()
export default apiService