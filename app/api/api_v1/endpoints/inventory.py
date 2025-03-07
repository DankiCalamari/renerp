from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
from app.services import inventory

router = APIRouter()

# Category endpoints
@router.get("/categories", response_model=List[schemas.Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve categories.
    """
    categories = inventory.get_categories(db, skip=skip, limit=limit)
    return categories

@router.post("/categories", response_model=schemas.Category)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: schemas.CategoryCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new category.
    """
    category = inventory.create_category(db, category_in)
    return category

@router.put("/categories/{category_id}", response_model=schemas.Category)
def update_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    category_in: schemas.CategoryUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a category.
    """
    category = inventory.update_category(db, category_id, category_in)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Product endpoints
@router.get("/products", response_model=List[schemas.Product])
def read_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve products.
    """
    products = inventory.get_products(db, skip=skip, limit=limit)
    return products

@router.post("/products", response_model=schemas.Product)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: schemas.ProductCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new product.
    """
    product = inventory.create_product(db, product_in)
    return product

@router.put("/products/{product_id}", response_model=schemas.Product)
def update_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    product_in: schemas.ProductUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a product.
    """
    product = inventory.update_product(db, product_id, product_in)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Stock endpoints
@router.get("/stock/{product_id}", response_model=schemas.Stock)
def read_stock(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get stock information for a product.
    """
    stock = inventory.get_stock_by_product(db, product_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

@router.post("/stock", response_model=schemas.Stock)
def create_stock(
    *,
    db: Session = Depends(deps.get_db),
    stock_in: schemas.StockCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new stock entry.
    """
    stock = inventory.create_stock(db, stock_in)
    return stock

# Stock Movement endpoints
@router.post("/stock-movements", response_model=schemas.StockMovement)
def create_stock_movement(
    *,
    db: Session = Depends(deps.get_db),
    movement_in: schemas.StockMovementCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new stock movement.
    """
    movement = inventory.create_stock_movement(db, movement_in, current_user.id)
    return movement

@router.get("/stock-movements/{product_id}", response_model=List[schemas.StockMovement])
def read_stock_movements(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve stock movements for a product.
    """
    movements = inventory.get_stock_movements(db, product_id, skip=skip, limit=limit)
    return movements 