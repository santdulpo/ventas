from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from database import get_supabase_client
from models import CategoryResponse, CategoryCreate
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

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    supabase: Client = Depends(get_supabase_client)
):
    """
    Crea una nueva categoría.
    """
    try:
        # Verificar que el slug no exista
        existing = supabase.table("categories").select("id").eq("slug", category.slug).execute()
        if existing.data:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe una categoría con el slug '{category.slug}'"
            )
        
        # Crear la categoría
        response = supabase.table("categories").insert(category.dict()).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Error al crear la categoría"
            )
        
        return response.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear categoría: {str(e)}"
        )

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: str,
    category: CategoryCreate,
    supabase: Client = Depends(get_supabase_client)
):
    """
    Actualiza una categoría existente.
    """
    try:
        # Verificar que la categoría existe
        existing = supabase.table("categories").select("id").eq("id", category_id).execute()
        if not existing.data:
            raise HTTPException(
                status_code=404,
                detail="Categoría no encontrada"
            )
        
        # Verificar que el slug no esté en uso por otra categoría
        slug_check = supabase.table("categories").select("id").eq("slug", category.slug).neq("id", category_id).execute()
        if slug_check.data:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe otra categoría con el slug '{category.slug}'"
            )
        
        # Actualizar la categoría
        response = supabase.table("categories").update(category.dict()).eq("id", category_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar la categoría"
            )
        
        return response.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar categoría: {str(e)}"
        )

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: str,
    supabase: Client = Depends(get_supabase_client)
):
    """
    Elimina una categoría.
    Nota: Solo se puede eliminar si no tiene productos asociados.
    """
    try:
        # Verificar que la categoría existe
        existing = supabase.table("categories").select("id").eq("id", category_id).execute()
        if not existing.data:
            raise HTTPException(
                status_code=404,
                detail="Categoría no encontrada"
            )
        
        # Verificar que no tenga productos asociados
        products = supabase.table("products").select("id").eq("category_id", category_id).execute()
        if products.data:
            raise HTTPException(
                status_code=400,
                detail=f"No se puede eliminar la categoría porque tiene {len(products.data)} productos asociados"
            )
        
        # Eliminar la categoría
        response = supabase.table("categories").delete().eq("id", category_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Error al eliminar la categoría"
            )
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar categoría: {str(e)}"
        )
