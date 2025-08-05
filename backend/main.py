import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import categories

app = FastAPI(
    title="DulProMax API",
    description="API para plataforma B2B de alimentos saludables",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ventasalimentos.netlify.app",  # Tu dominio de Netlify
        "http://localhost:3000",               # Para desarrollo local
        "http://localhost:5173",               # Vite dev server
        "http://localhost:8080",               # Vue CLI dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(categories.router, prefix="/api/v1")
@app.get("/")
async def root():
    return {"message": "¡Bienvenido a DulProMax API!", "status": "success", "version": "1.1.0", "build": "2024-12-19"}

@app.get("/ping")
async def ping():
    return {"message": "pong", "timestamp": "2024-01-01T00:00:00Z"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "dulpromax-api", "version": "1.0.0"}

# Nuevo endpoint para datos de prueba
@app.get("/api/productos")
async def get_productos():
    return {
        "productos": [
            {"id": 1, "nombre": "Quinoa Orgánica", "precio": 15.50, "categoria": "granos"},
            {"id": 2, "nombre": "Aceite de Coco", "precio": 8.99, "categoria": "aceites"},
            {"id": 3, "nombre": "Miel Pura", "precio": 12.00, "categoria": "endulzantes"}
        ],
        "total": 3
    }

@app.get("/api/stats")
async def get_stats():
    return {
        "ventas_mes": 1250,
        "productos_activos": 45,
        "clientes_registrados": 128,
        "pedidos_pendientes": 8
    }

# ===== INTEGRACIÓN CON SUPABASE =====
from supabase_config import supabase

@app.get("/api/test-supabase")
async def test_supabase_connection():
    """Probar conexión con Supabase"""
    try:
        # Intentar hacer una consulta simple
        response = supabase.table("test").select("*").limit(1).execute()
        return {
            "status": "success",
            "message": "Conexión exitosa con Supabase",
            "supabase_url": supabase.supabase_url,
            "connected": True
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Error conectando con Supabase: {str(e)}",
            "connected": False
        }

@app.get("/api/supabase-info")
async def get_supabase_info():
    """Información de configuración de Supabase"""
    return {
        "supabase_url": supabase.supabase_url,
        "configured": bool(supabase.supabase_url),
        "version": "2.8.1"
    }

# Punto de entrada para Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
