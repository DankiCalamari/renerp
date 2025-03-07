from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
from app.services import sales

router = APIRouter()

# Customer endpoints
@router.get("/customers", response_model=List[schemas.Customer])
def read_customers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve customers.
    """
    customers = sales.get_customers(db, skip=skip, limit=limit)
    return customers

@router.post("/customers", response_model=schemas.Customer)
def create_customer(
    *,
    db: Session = Depends(deps.get_db),
    customer_in: schemas.CustomerCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new customer.
    """
    customer = sales.create_customer(db, customer_in)
    return customer

@router.put("/customers/{customer_id}", response_model=schemas.Customer)
def update_customer(
    *,
    db: Session = Depends(deps.get_db),
    customer_id: int,
    customer_in: schemas.CustomerUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a customer.
    """
    customer = sales.update_customer(db, customer_id, customer_in)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

# Order endpoints
@router.get("/orders", response_model=List[schemas.Order])
def read_orders(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve orders.
    """
    orders = sales.get_orders(db, skip=skip, limit=limit)
    return orders

@router.post("/orders", response_model=schemas.Order)
def create_order(
    *,
    db: Session = Depends(deps.get_db),
    order_in: schemas.OrderCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new order.
    """
    try:
        order = sales.create_order(db, order_in, current_user.id)
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/orders/{order_id}", response_model=schemas.Order)
def update_order(
    *,
    db: Session = Depends(deps.get_db),
    order_id: int,
    order_in: schemas.OrderUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an order.
    """
    try:
        order = sales.update_order(db, order_id, order_in, current_user.id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Invoice endpoints
@router.post("/invoices", response_model=schemas.Invoice)
def create_invoice(
    *,
    db: Session = Depends(deps.get_db),
    invoice_in: schemas.InvoiceCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new invoice.
    """
    try:
        invoice = sales.create_invoice(db, invoice_in, current_user.id)
        return invoice
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/invoices/{invoice_id}", response_model=schemas.Invoice)
def update_invoice(
    *,
    db: Session = Depends(deps.get_db),
    invoice_id: int,
    invoice_in: schemas.InvoiceUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an invoice.
    """
    invoice = sales.update_invoice(db, invoice_id, invoice_in)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

# Payment endpoints
@router.post("/payments", response_model=schemas.Payment)
def create_payment(
    *,
    db: Session = Depends(deps.get_db),
    payment_in: schemas.PaymentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new payment.
    """
    try:
        payment = sales.create_payment(db, payment_in, current_user.id)
        return payment
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/payments/{invoice_id}", response_model=List[schemas.Payment])
def read_payments(
    *,
    db: Session = Depends(deps.get_db),
    invoice_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve payments for an invoice.
    """
    payments = sales.get_payments(db, invoice_id, skip=skip, limit=limit)
    return payments 