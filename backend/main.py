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
    return {
        "message": "¡Bienvenido a DulProMax API!", 
        "status": "success", 
        "version": "1.0.0", 
        "description": "API para plataforma B2B de alimentos saludables"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "dulpromax-api", 
        "version": "1.0.0"
    }

# Punto de entrada para Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
