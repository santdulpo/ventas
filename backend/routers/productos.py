from fastapi import APIRouter, HTTPException
from typing import List, Optional
from models.producto import Producto, ProductoCreate, ProductoResponse, CategoriaProducto

router = APIRouter(prefix="/api/productos", tags=["productos"])

# Base de datos temporal con productos de muestra
productos_db = [
    {
        "id": 1,
        "nombre": "Confites de Quinoa",
        "descripcion": "Deliciosos confites elaborados con quinoa orgánica",
        "categoria": "confites_saludables",
        "precio_base": 15.50,
        "stock": 100,
        "imagen_url": "/images/confites-quinoa.jpg",
        "activo": True,
        "precio_tienda_saludable": 13.18,  # 15% descuento
        "precio_distribuidor": 11.63,      # 25% descuento
        "precio_gimnasio": 13.64,          # 12% descuento
        "precio_cafeteria": 13.95          # 10% descuento
    },
    {
        "id": 2,
        "nombre": "Pan Integral Multicereal",
        "descripcion": "Pan artesanal con mezcla de cereales integrales",
        "categoria": "panaderia",
        "precio_base": 8.99,
        "stock": 50,
        "imagen_url": "/images/pan-integral.jpg",
        "activo": True,
        "precio_tienda_saludable": 7.64,
        "precio_distribuidor": 6.74,
        "precio_gimnasio": 7.91,
        "precio_cafeteria": 8.09
    },
    {
        "id": 3,
        "nombre": "Granola Premium",
        "descripcion": "Granola casera con frutos secos y miel pura",
        "categoria": "cereales_granolas",
        "precio_base": 12.00,
        "stock": 75,
        "imagen_url": "/images/granola-premium.jpg",
        "activo": True,
        "precio_tienda_saludable": 10.20,
        "precio_distribuidor": 9.00,
        "precio_gimnasio": 10.56,
        "precio_cafeteria": 10.80
    },
    {
        "id": 4,
        "nombre": "Barras de Proteína",
        "descripcion": "Barras energéticas con proteína vegetal",
        "categoria": "barras_cereal",
        "precio_base": 18.50,
        "stock": 120,
        "imagen_url": "/images/barras-proteina.jpg",
        "activo": True,
        "precio_tienda_saludable": 15.73,
        "precio_distribuidor": 13.88,
        "precio_gimnasio": 16.28,
        "precio_cafeteria": 16.65
    }
]

@router.get("/", response_model=List[ProductoResponse])
async def get_productos(categoria: Optional[CategoriaProducto] = None):
    """Obtener todos los productos, opcionalmente filtrados por categoría"""
    productos = productos_db
    if categoria:
        productos = [p for p in productos_db if p["categoria"] == categoria]
    return productos

@router.get("/{producto_id}", response_model=ProductoResponse)
async def get_producto(producto_id: int):
    """Obtener un producto específico"""
    producto = next((p for p in productos_db if p["id"] == producto_id), None)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.get("/categoria/{categoria}", response_model=List[ProductoResponse])
async def get_productos_por_categoria(categoria: CategoriaProducto):
    """Obtener productos por categoría específica"""
    productos = [p for p in productos_db if p["categoria"] == categoria]
    return productos

@router.post("/", response_model=ProductoResponse)
async def create_producto(producto: ProductoCreate):
    """Crear un nuevo producto"""
    nuevo_id = max([p["id"] for p in productos_db]) + 1 if productos_db else 1
    
    # Calcular precios diferenciados automáticamente
    precio_base = producto.precio_base
    nuevo_producto = {
        "id": nuevo_id,
        **producto.dict(),
        "activo": True,
        "precio_tienda_saludable": round(precio_base * 0.85, 2),  # 15% desc
        "precio_distribuidor": round(precio_base * 0.75, 2),      # 25% desc
        "precio_gimnasio": round(precio_base * 0.88, 2),          # 12% desc
        "precio_cafeteria": round(precio_base * 0.90, 2)          # 10% desc
    }
    
    productos_db.append(nuevo_producto)
    return nuevo_producto
