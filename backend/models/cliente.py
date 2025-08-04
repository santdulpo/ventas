from enum import Enum
from pydantic import BaseModel
from typing import Optional

class TipoCliente(str, Enum):
    TIENDA_SALUDABLE = "tienda_saludable"
    DISTRIBUIDOR = "distribuidor" 
    GIMNASIO = "gimnasio"
    CAFETERIA = "cafeteria"

class Cliente(BaseModel):
    id: Optional[int] = None
    nombre: str
    email: str
    tipo_cliente: TipoCliente
    telefono: str
    direccion: str
    ciudad: str
    descuento_base: float = 0.0  # Descuento según tipo de cliente
    
class ClienteCreate(BaseModel):
    nombre: str
    email: str
    tipo_cliente: TipoCliente
    telefono: str
    direccion: str
    ciudad: str

class ClienteResponse(BaseModel):
    id: int
    nombre: str
    email: str
    tipo_cliente: TipoCliente
    telefono: str
    direccion: str
    ciudad: str
    descuento_base: float
