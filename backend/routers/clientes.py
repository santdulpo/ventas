from fastapi import APIRouter, HTTPException
from typing import List
from models.cliente import Cliente, ClienteCreate, ClienteResponse, TipoCliente

router = APIRouter(prefix="/api/clientes", tags=["clientes"])

# Base de datos temporal (en memoria)
clientes_db = [
    {
        "id": 1,
        "nombre": "Tienda Vida Sana",
        "email": "info@vidasana.com",
        "tipo_cliente": "tienda_saludable",
        "telefono": "123-456-7890",
        "direccion": "Av. Principal 123",
        "ciudad": "Bogotá",
        "descuento_base": 0.15
    },
    {
        "id": 2,
        "nombre": "Distribuidora El Sol",
        "email": "ventas@elsol.com",
        "tipo_cliente": "distribuidor",
        "telefono": "098-765-4321",
        "direccion": "Calle 45 #23-67",
        "ciudad": "Medellín",
        "descuento_base": 0.25
    }
]

@router.get("/", response_model=List[ClienteResponse])
async def get_clientes():
    """Obtener todos los clientes B2B"""
    return clientes_db

@router.get("/{cliente_id}", response_model=ClienteResponse)
async def get_cliente(cliente_id: int):
    """Obtener un cliente específico"""
    cliente = next((c for c in clientes_db if c["id"] == cliente_id), None)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.post("/", response_model=ClienteResponse)
async def create_cliente(cliente: ClienteCreate):
    """Crear un nuevo cliente B2B"""
    nuevo_id = max([c["id"] for c in clientes_db]) + 1 if clientes_db else 1
    
    # Asignar descuento base según tipo de cliente
    descuentos = {
        "tienda_saludable": 0.15,
        "distribuidor": 0.25,
        "gimnasio": 0.12,
        "cafeteria": 0.10
    }
    
    nuevo_cliente = {
        "id": nuevo_id,
        **cliente.dict(),
        "descuento_base": descuentos.get(cliente.tipo_cliente, 0.0)
    }
    
    clientes_db.append(nuevo_cliente)
    return nuevo_cliente

@router.get("/tipo/{tipo_cliente}", response_model=List[ClienteResponse])
async def get_clientes_por_tipo(tipo_cliente: TipoCliente):
    """Obtener clientes filtrados por tipo"""
    clientes_filtrados = [c for c in clientes_db if c["tipo_cliente"] == tipo_cliente]
    return clientes_filtrados
