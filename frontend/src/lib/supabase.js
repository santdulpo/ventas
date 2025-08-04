import { createClient } from '@supabase/supabase-js'

// Configuración de Supabase desde variables de entorno
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

// Crear cliente de Supabase
export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Función para verificar conexión
export const testConnection = async () => {
  try {
    const { data, error } = await supabase.from('test').select('*').limit(1)
    if (error && error.code !== 'PGRST116') { // PGRST116 = tabla no existe
      throw error
    }
    return { success: true, message: 'Conexión exitosa con Supabase' }
  } catch (error) {
    return { success: false, message: error.message }
  }
}
