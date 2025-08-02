import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

// Crear la aplicación Vue
const app = createApp(App)

// Configurar Pinia para gestión de estado
const pinia = createPinia()
app.use(pinia)

// Montar la aplicación
app.mount('#app')

console.log('🚀 DulProMax B2B - Frontend iniciado correctamente')
