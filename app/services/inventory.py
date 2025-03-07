from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.inventory import Category, Product, Stock, StockMovement
from app.schemas.inventory import (
    CategoryCreate, CategoryUpdate,
    ProductCreate, ProductUpdate,
    StockCreate, StockUpdate,
    StockMovementCreate
)

# Category services
def get_category(db: Session, category_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()

def get_categories(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Category]:
    return db.query(Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: CategoryCreate) -> Category:
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(
    db: Session, category_id: int, category: CategoryUpdate
) -> Optional[Category]:
    db_category = get_category(db, category_id)
    if not db_category:
        return None
    
    update_data = category.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Product services
def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()

def get_product_by_sku(db: Session, sku: str) -> Optional[Product]:
    return db.query(Product).filter(Product.sku == sku).first()

def get_products(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Product]:
    return db.query(Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(
    db: Session, product_id: int, product: ProductUpdate
) -> Optional[Product]:
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    
    update_data = product.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Stock services
def get_stock(db: Session, stock_id: int) -> Optional[Stock]:
    return db.query(Stock).filter(Stock.id == stock_id).first()

def get_stock_by_product(db: Session, product_id: int) -> Optional[Stock]:
    return db.query(Stock).filter(Stock.product_id == product_id).first()

def create_stock(db: Session, stock: StockCreate) -> Stock:
    db_stock = Stock(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def update_stock(
    db: Session, stock_id: int, stock: StockUpdate
) -> Optional[Stock]:
    db_stock = get_stock(db, stock_id)
    if not db_stock:
        return None
    
    update_data = stock.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_stock, field, value)
    
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

# Stock Movement services
def create_stock_movement(
    db: Session, movement: StockMovementCreate, user_id: int
) -> StockMovement:
    db_movement = StockMovement(**movement.dict(), created_by=user_id)
    
    # Update stock quantity
    stock = get_stock_by_product(db, movement.product_id)
    if not stock:
        stock = Stock(
            product_id=movement.product_id,
            quantity=0,
            location="default"
        )
        db.add(stock)
    
    if movement.movement_type == "in":
        stock.quantity += movement.quantity
    else:
        stock.quantity -= movement.quantity
    
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement

def get_stock_movements(
    db: Session, product_id: int, skip: int = 0, limit: int = 100
) -> List[StockMovement]:
    return (
        db.query(StockMovement)
        .filter(StockMovement.product_id == product_id)
        .offset(skip)
        .limit(limit)
        .all()
    ) 