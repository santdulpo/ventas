from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import List, Optional
from database import get_supabase_client
from models import ProductResponse, ProductCreate, ProductsListResponse
from supabase import Client
import math

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=ProductsListResponse)
async def get_products(
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(20, ge=1, le=100, description="Productos por página"),
    category_id: Optional[str] = Query(None, description="Filtrar por categoría"),
    search: Optional[str] = Query(None, description="Buscar por nombre o descripción"),
    active_only: bool = Query(True, description="Solo productos activos"),
    featured_only: bool = Query(False, description="Solo productos destacados"),
    min_price: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    supabase: Client = Depends(get_supabase_client)
):
    """
    Obtiene todos los productos con paginación y filtros.
    """
    try:
        # Construir query base
        query = supabase.table("products").select("""
            *,
            category:categories(id, name, slug)
        """)
        
        # Aplicar filtros
        if active_only:
            query = query.eq("is_active", True)
            
        if featured_only:
            query = query.eq("is_featured", True)
            
        if category_id:
            query = query.eq("category_id", category_id)
            
        if search:
            query = query.or_(f"name.ilike.%{search}%,description.ilike.%{search}%")
            
        if min_price is not None:
            query = query.gte("price_wholesale", min_price)
            
        if max_price is not None:
            query = query.lte("price_wholesale", max_price)
        
        # Contar total de productos (para paginación)
        count_response = query.execute()
        total = len(count_response.data) if count_response.data else 0
        
        # Aplicar paginación
        offset = (page - 1) * per_page
        query = query.order("created_at", desc=True).range(offset, offset + per_page - 1)
        
        response = query.execute()
        
        products = response.data if response.data else []
        total_pages = math.ceil(total / per_page)
        
        return ProductsListResponse(
            products=products,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener productos: {str(e)}"
        )

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    supabase: Client = Depends(get_supabase_client)
):
    """
    Obtiene un producto específico por ID.
    """
    try:
        response = supabase.table("products").select("""
            *,
            category:categories(id, name, slug)
        """).eq("id", product_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )
        
        return response.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener producto: {str(e)}"
        )

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    supabase: Client = Depends(get_supabase_client)
):
    """
    Crea un nuevo producto.
    """
    try:
        # Verificar que el slug no exista
        if product.slug:
            existing = supabase.table("products").select("id").eq("slug", product.slug).execute()
            if existing.data:
                raise HTTPException(
                    status_code=400,
                    detail=f"Ya existe un producto con el slug '{product.slug}'"
                )
        
        # Verificar que el SKU no exista (si se proporciona)
        if product.sku:
            existing_sku = supabase.table("products").select("id").eq("sku", product.sku).execute()
            if existing_sku.data:
                raise HTTPException(
                    status_code=400,
                    detail=f"Ya existe un producto con el SKU '{product.sku}'"
                )
        
        # Verificar que la categoría existe (si se proporciona)
        if product.category_id:
            category = supabase.table("categories").select("id").eq("id", product.category_id).execute()
            if not category.data:
                raise HTTPException(
                    status_code=400,
                    detail="La categoría especificada no existe"
                )
        
        # Crear el producto
        response = supabase.table("products").insert(product.dict()).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Error al crear el producto"
            )
        
        # Obtener el producto creado con la categoría
        created_product = supabase.table("products").select("""
            *,
            category:categories(id, name, slug)
        """).eq("id", response.data[0]["id"]).execute()
        
        return created_product.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear producto: {str(e)}"
        )

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product: ProductCreate,
    supabase: Client = Depends(get_supabase_client)
):
    """
    Actualiza un producto existente.
    """
    try:
        # Verificar que el producto existe
        existing = supabase.table("products").select("id").eq("id", product_id).execute()
        if not existing.data:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )
        
        # Verificar que el slug no esté en uso por otro producto
        if product.slug:
            slug_check = supabase.table("products").select("id").eq("slug", product.slug).neq("id", product_id).execute()
            if slug_check.data:
                raise HTTPException(
                    status_code=400,
                    detail=f"Ya existe otro producto con el slug '{product.slug}'"
                )
        
        # Verificar que el SKU no esté en uso por otro producto
        if product.sku:
            sku_check = supabase.table("products").select("id").eq("sku", product.sku).neq("id", product_id).execute()
            if sku_check.data:
                raise HTTPException(
                    status_code=400,
                    detail=f"Ya existe otro producto con el SKU '{product.sku}'"
                )
        
        # Verificar que la categoría existe (si se proporciona)
        if product.category_id:
            category = supabase.table("categories").select("id").eq("id", product.category_id).execute()
            if not category.data:
                raise HTTPException(
                    status_code=400,
                    detail="La categoría especificada no existe"
                )
        
        # Actualizar el producto
        response = supabase.table("products").update(product.dict()).eq("id", product_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar el producto"
            )
        
        # Obtener el producto actualizado con la categoría
        updated_product = supabase.table("products").select("""
            *,
            category:categories(id, name, slug)
        """).eq("id", product_id).execute()
        
        return updated_product.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar producto: {str(e)}"
        )

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    supabase: Client = Depends(get_supabase_client)
):
    """
    Elimina un producto.
    """
    try:
        # Verificar que el producto existe
        existing = supabase.table("products").select("id").eq("id", product_id).execute()
        if not existing.data:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )
        
        # Eliminar el producto
        response = supabase.table("products").delete().eq("id", product_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Error al eliminar el producto"
            )
        
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar producto: {str(e)}"
        )

@router.patch("/{product_id}/stock", response_model=ProductResponse)
async def update_product_stock(
    product_id: str,
    new_stock: int = Query(..., ge=0, description="Nueva cantidad en stock"),
    supabase: Client = Depends(get_supabase_client)
):
    """
    Actualiza solo el stock de un producto.
    """
    try:
        # Verificar que el producto existe
        existing = supabase.table("products").select("id").eq("id", product_id).execute()
        if not existing.data:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )
        
        # Actualizar solo el stock
        response = supabase.table("products").update({
            "stock_quantity": new_stock
        }).eq("id", product_id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar el stock"
            )
        
        # Obtener el producto actualizado
        updated_product = supabase.table("products").select("""
            *,
            category:categories(id, name, slug)
        """).eq("id", product_id).execute()
        
        return updated_product.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar stock: {str(e)}"
        )
