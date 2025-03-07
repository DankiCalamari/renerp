from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
from app.services import purchase

router = APIRouter()

# Supplier endpoints
@router.get("/suppliers", response_model=List[schemas.Supplier])
def read_suppliers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve suppliers.
    """
    suppliers = purchase.get_suppliers(db, skip=skip, limit=limit)
    return suppliers

@router.post("/suppliers", response_model=schemas.Supplier)
def create_supplier(
    *,
    db: Session = Depends(deps.get_db),
    supplier_in: schemas.SupplierCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new supplier.
    """
    supplier = purchase.create_supplier(db, supplier_in)
    return supplier

@router.put("/suppliers/{supplier_id}", response_model=schemas.Supplier)
def update_supplier(
    *,
    db: Session = Depends(deps.get_db),
    supplier_id: int,
    supplier_in: schemas.SupplierUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a supplier.
    """
    supplier = purchase.update_supplier(db, supplier_id, supplier_in)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

# Purchase Order endpoints
@router.get("/orders", response_model=List[schemas.PurchaseOrder])
def read_purchase_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve purchase orders.
    """
    orders = purchase.get_purchase_orders(db, skip=skip, limit=limit)
    return orders

@router.post("/orders", response_model=schemas.PurchaseOrder)
def create_purchase_order(
    *,
    db: Session = Depends(deps.get_db),
    order_in: schemas.PurchaseOrderCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new purchase order.
    """
    try:
        order = purchase.create_purchase_order(db, order_in, current_user.id)
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/orders/{order_id}", response_model=schemas.PurchaseOrder)
def update_purchase_order(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    order_in: schemas.PurchaseOrderUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a purchase order.
    """
    try:
        order = purchase.update_purchase_order(db, order_id, order_in, current_user.id)
        if not order:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Purchase Receipt endpoints
@router.post("/receipts", response_model=schemas.PurchaseReceipt)
def create_purchase_receipt(
    *,
    db: Session = Depends(deps.get_db),
    receipt_in: schemas.PurchaseReceiptCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new purchase receipt.
    """
    try:
        receipt = purchase.create_purchase_receipt(db, receipt_in, current_user.id)
        return receipt
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/receipts/{receipt_id}", response_model=schemas.PurchaseReceipt)
def update_purchase_receipt(
    *,
    db: Session = Depends(deps.get_db),
    receipt_id: int,
    receipt_in: schemas.PurchaseReceiptUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a purchase receipt.
    """
    try:
        receipt = purchase.update_purchase_receipt(db, receipt_id, receipt_in)
        if not receipt:
            raise HTTPException(status_code=404, detail="Purchase receipt not found")
        return receipt
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 