from fastapi import APIRouter, HTTPException, Depends
from typing import List
from database import get_supabase_client
from models import CategoryResponse
from supabase import Client

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    active_only: bool = True,
    supabase: Client = Depends(get_supabase_client)
):
    """
    Obtiene todas las categorías de productos.
    
    - **active_only**: Si es True, solo retorna categorías activas
    """
    try:
        query = supabase.table("categories").select("*")
        
        if active_only:
            query = query.eq("is_active", True)
        
        query = query.order("name")
        
        response = query.execute()
        
        if response.data is None:
            return []
            
        return response.data
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al obtener categorías: {str(e)}"
        )

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: str,
    supabase: Client = Depends(get_supabase_client)
):
    """
    Obtiene una categoría específica por ID.
    """
    try:
        response = supabase.table("categories").select("*").eq("id", category_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=404, 
                detail="Categoría no encontrada"
            )
        
        return response.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al obtener categoría: {str(e)}"
        )
