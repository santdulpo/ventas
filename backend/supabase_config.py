import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Crear cliente de Supabase
def get_supabase_client() -> Client:
    """Crear y retornar cliente de Supabase"""
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise ValueError("SUPABASE_URL y SUPABASE_ANON_KEY deben estar configuradas en .env")
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    return supabase

# Cliente global para usar en toda la aplicación
supabase = get_supabase_client()
