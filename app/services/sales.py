from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.sales import Customer, Order, OrderItem, Invoice, Payment
from app.models.inventory import Product
from app.schemas.sales import (
    CustomerCreate, CustomerUpdate,
    OrderCreate, OrderUpdate,
    OrderItemCreate,
    InvoiceCreate, InvoiceUpdate,
    PaymentCreate
)
from datetime import datetime, timedelta

# Customer services
def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.id == customer_id).first()

def get_customer_by_email(db: Session, email: str) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.email == email).first()

def get_customers(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Customer]:
    return db.query(Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(
    db: Session, customer_id: int, customer: CustomerUpdate
) -> Optional[Customer]:
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
    
    update_data = customer.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_customer, field, value)
    
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# Order services
def get_order(db: Session, order_id: int) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()

def get_order_by_number(db: Session, order_number: str) -> Optional[Order]:
    return db.query(Order).filter(Order.order_number == order_number).first()

def get_orders(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Order]:
    return db.query(Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: OrderCreate, user_id: int) -> Order:
    # Calculate total amount
    total_amount = 0
    order_items = []
    
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise ValueError(f"Product {item.product_id} not found")
        
        item_total = (item.quantity * item.unit_price) * (1 - item.discount)
        total_amount += item_total
        
        order_item = OrderItem(
            **item.dict(),
            total_amount=item_total
        )
        order_items.append(order_item)
    
    # Create order
    db_order = Order(
        **order.dict(exclude={'items'}),
        total_amount=total_amount,
        created_by=user_id
    )
    db.add(db_order)
    db.flush()  # Get order ID
    
    # Add order items
    for item in order_items:
        item.order_id = db_order.id
        db.add(item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(
    db: Session, order_id: int, order: OrderUpdate, user_id: int
) -> Optional[Order]:
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    
    # Update order fields
    update_data = order.dict(exclude={'items'}, exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_order, field, value)
    
    # Update items if provided
    if order.items:
        # Delete existing items
        db.query(OrderItem).filter(OrderItem.order_id == order_id).delete()
        
        # Calculate new total
        total_amount = 0
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise ValueError(f"Product {item.product_id} not found")
            
            item_total = (item.quantity * item.unit_price) * (1 - item.discount)
            total_amount += item_total
            
            order_item = OrderItem(
                **item.dict(),
                order_id=order_id,
                total_amount=item_total
            )
            db.add(order_item)
        
        db_order.total_amount = total_amount
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# Invoice services
def get_invoice(db: Session, invoice_id: int) -> Optional[Invoice]:
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()

def get_invoice_by_number(db: Session, invoice_number: str) -> Optional[Invoice]:
    return db.query(Invoice).filter(Invoice.invoice_number == invoice_number).first()

def create_invoice(db: Session, invoice: InvoiceCreate, user_id: int) -> Invoice:
    # Verify order exists and is confirmed
    order = db.query(Order).filter(Order.id == invoice.order_id).first()
    if not order:
        raise ValueError(f"Order {invoice.order_id} not found")
    if order.status != OrderStatus.CONFIRMED:
        raise ValueError("Order must be confirmed before creating invoice")
    
    db_invoice = Invoice(**invoice.dict(), created_by=user_id)
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def update_invoice(
    db: Session, invoice_id: int, invoice: InvoiceUpdate
) -> Optional[Invoice]:
    db_invoice = get_invoice(db, invoice_id)
    if not db_invoice:
        return None
    
    update_data = invoice.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_invoice, field, value)
    
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

# Payment services
def create_payment(db: Session, payment: PaymentCreate, user_id: int) -> Payment:
    # Verify invoice exists
    invoice = db.query(Invoice).filter(Invoice.id == payment.invoice_id).first()
    if not invoice:
        raise ValueError(f"Invoice {payment.invoice_id} not found")
    
    # Create payment
    db_payment = Payment(**payment.dict(), created_by=user_id)
    db.add(db_payment)
    
    # Update invoice payment status
    total_paid = sum(p.amount for p in invoice.payments) + payment.amount
    if total_paid >= invoice.total_amount:
        invoice.payment_status = PaymentStatus.PAID
    elif total_paid > 0:
        invoice.payment_status = PaymentStatus.PARTIAL
    
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payments(
    db: Session, invoice_id: int, skip: int = 0, limit: int = 100
) -> List[Payment]:
    return (
        db.query(Payment)
        .filter(Payment.invoice_id == invoice_id)
        .offset(skip)
        .limit(limit)
        .all()
    ) 