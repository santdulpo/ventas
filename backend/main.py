from fastapi import FastAPI

app = FastAPI(
    title="DulProMax API",
    description="API para plataforma B2B de alimentos saludables",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "¡Bienvenido a DulProMax API!"}

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "dulpromax-api"} 