from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    slug: str = Field(..., max_length=100)
    image_url: Optional[str] = None
    is_active: bool = True

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    slug: str = Field(..., max_length=200)
    sku: Optional[str] = Field(None, max_length=50)
    category_id: Optional[UUID] = None
    
    # Precios B2B
    price_retail: float = Field(..., gt=0)
    price_wholesale: float = Field(..., gt=0)
    price_gym: Optional[float] = Field(None, gt=0)
    price_cafeteria: Optional[float] = Field(None, gt=0)
    price_store: Optional[float] = Field(None, gt=0)
    
    # Información del producto
    weight_grams: Optional[int] = Field(None, gt=0)
    dimensions_cm: Optional[str] = None
    ingredients: Optional[str] = None
    nutritional_info: Optional[Dict[str, Any]] = None
    allergens: Optional[List[str]] = None
    
    # Inventario
    stock_quantity: int = Field(default=0, ge=0)
    min_stock_alert: int = Field(default=10, ge=0)
    max_order_quantity: Optional[int] = Field(None, gt=0)
    min_order_quantity: int = Field(default=1, gt=0)
    
    # Imágenes
    main_image_url: Optional[str] = None
    gallery_images: Optional[List[str]] = None
    
    # Metadatos
    is_active: bool = True
    is_featured: bool = False
    tags: Optional[List[str]] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True

class ProductsListResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
