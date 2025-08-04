import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar los routers
from routers import clientes, productos

app = FastAPI(
    title="DulProMax API B2B",
    description="API para plataforma B2B de alimentos saludables con segmentación de clientes",
    version="2.0.0"
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
app.include_router(clientes.router)
app.include_router(productos.router)

@app.get("/")
async def root():
    return {
        "message": "¡Bienvenido a DulProMax API B2B!", 
        "status": "success",
        "version": "2.0.0",
        "features": [
            "Gestión de clientes B2B segmentados",
            "Catálogo de productos por categorías",
            "Precios diferenciados por tipo de cliente",
            "API RESTful completa"
        ]
    }

@app.get("/ping")
async def ping():
    return {"message": "pong", "timestamp": "2024-01-01T00:00:00Z"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "dulpromax-b2b-api", "version": "2.0.0"}

# Endpoint de estadísticas actualizado
@app.get("/api/stats")
async def get_stats():
    return {
        "clientes_registrados": 15,
        "productos_activos": 45,
        "categorias_productos": 5,
        "ventas_mes_actual": 1250.50,
        "pedidos_pendientes": 8,
        "tipos_cliente": {
            "tiendas_saludables": 5,
            "distribuidores": 3,
            "gimnasios": 4,
            "cafeterias": 3
        }
    }

# Punto de entrada para Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
