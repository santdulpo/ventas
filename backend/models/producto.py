from enum import Enum
from pydantic import BaseModel
from typing import Optional, List

class CategoriaProducto(str, Enum):
    CONFITES_SALUDABLES = "confites_saludables"
    PANADERIA = "panaderia"
    CEREALES_GRANOLAS = "cereales_granolas"
    BARRAS_CEREAL = "barras_cereal"
    DULCES_DIETETICOS = "dulces_dieteticos"

class Producto(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: str
    categoria: CategoriaProducto
    precio_base: float
    stock: int
    imagen_url: Optional[str] = None
    activo: bool = True
    
    # Precios diferenciados por tipo de cliente
    precio_tienda_saludable: Optional[float] = None
    precio_distribuidor: Optional[float] = None
    precio_gimnasio: Optional[float] = None
    precio_cafeteria: Optional[float] = None

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: str
    categoria: CategoriaProducto
    precio_base: float
    stock: int
    imagen_url: Optional[str] = None

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    categoria: CategoriaProducto
    precio_base: float
    stock: int
    imagen_url: Optional[str]
    activo: bool
    precio_tienda_saludable: Optional[float]
    precio_distribuidor: Optional[float]
    precio_gimnasio: Optional[float]
    precio_cafeteria: Optional[float]
