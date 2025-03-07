from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.purchase import (
    Supplier, PurchaseOrder, PurchaseOrderItem,
    PurchaseReceipt, PurchaseReceiptItem
)
from app.models.inventory import Product
from app.schemas.purchase import (
    SupplierCreate, SupplierUpdate,
    PurchaseOrderCreate, PurchaseOrderUpdate,
    PurchaseOrderItemCreate,
    PurchaseReceiptCreate, PurchaseReceiptUpdate,
    PurchaseReceiptItemCreate
)
from datetime import datetime

# Supplier services
def get_supplier(db: Session, supplier_id: int) -> Optional[Supplier]:
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()

def get_supplier_by_email(db: Session, email: str) -> Optional[Supplier]:
    return db.query(Supplier).filter(Supplier.email == email).first()

def get_suppliers(
    db: Session, skip: int = 0, limit: int = 100
) -> List[Supplier]:
    return db.query(Supplier).offset(skip).limit(limit).all()

def create_supplier(db: Session, supplier: SupplierCreate) -> Supplier:
    db_supplier = Supplier(**supplier.dict())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def update_supplier(
    db: Session, supplier_id: int, supplier: SupplierUpdate
) -> Optional[Supplier]:
    db_supplier = get_supplier(db, supplier_id)
    if not db_supplier:
        return None
    
    update_data = supplier.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_supplier, field, value)
    
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

# Purchase Order services
def get_purchase_order(db: Session, order_id: int) -> Optional[PurchaseOrder]:
    return db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()

def get_purchase_order_by_number(db: Session, order_number: str) -> Optional[PurchaseOrder]:
    return db.query(PurchaseOrder).filter(PurchaseOrder.order_number == order_number).first()

def get_purchase_orders(
    db: Session, skip: int = 0, limit: int = 100
) -> List[PurchaseOrder]:
    return db.query(PurchaseOrder).offset(skip).limit(limit).all()

def create_purchase_order(db: Session, order: PurchaseOrderCreate, user_id: int) -> PurchaseOrder:
    # Calculate total amount
    total_amount = 0
    order_items = []
    
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise ValueError(f"Product {item.product_id} not found")
        
        item_total = (item.quantity * item.unit_price) * (1 - item.discount)
        total_amount += item_total
        
        order_item = PurchaseOrderItem(
            **item.dict(),
            total_amount=item_total
        )
        order_items.append(order_item)
    
    # Create order
    db_order = PurchaseOrder(
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

def update_purchase_order(
    db: Session, order_id: int, order: PurchaseOrderUpdate, user_id: int
) -> Optional[PurchaseOrder]:
    db_order = get_purchase_order(db, order_id)
    if not db_order:
        return None
    
    # Update order fields
    update_data = order.dict(exclude={'items'}, exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_order, field, value)
    
    # Update items if provided
    if order.items:
        # Delete existing items
        db.query(PurchaseOrderItem).filter(PurchaseOrderItem.order_id == order_id).delete()
        
        # Calculate new total
        total_amount = 0
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise ValueError(f"Product {item.product_id} not found")
            
            item_total = (item.quantity * item.unit_price) * (1 - item.discount)
            total_amount += item_total
            
            order_item = PurchaseOrderItem(
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

# Purchase Receipt services
def get_purchase_receipt(db: Session, receipt_id: int) -> Optional[PurchaseReceipt]:
    return db.query(PurchaseReceipt).filter(PurchaseReceipt.id == receipt_id).first()

def get_purchase_receipt_by_number(db: Session, receipt_number: str) -> Optional[PurchaseReceipt]:
    return db.query(PurchaseReceipt).filter(PurchaseReceipt.receipt_number == receipt_number).first()

def create_purchase_receipt(db: Session, receipt: PurchaseReceiptCreate, user_id: int) -> PurchaseReceipt:
    # Verify order exists and is confirmed
    order = db.query(PurchaseOrder).filter(PurchaseOrder.id == receipt.order_id).first()
    if not order:
        raise ValueError(f"Purchase order {receipt.order_id} not found")
    if order.status != PurchaseOrderStatus.CONFIRMED:
        raise ValueError("Purchase order must be confirmed before creating receipt")
    
    # Calculate total amount
    total_amount = 0
    receipt_items = []
    
    for item in receipt.items:
        order_item = db.query(PurchaseOrderItem).filter(
            PurchaseOrderItem.id == item.order_item_id
        ).first()
        if not order_item:
            raise ValueError(f"Order item {item.order_item_id} not found")
        
        item_total = item.quantity * item.unit_price
        total_amount += item_total
        
        receipt_item = PurchaseReceiptItem(
            **item.dict(),
            total_amount=item_total
        )
        receipt_items.append(receipt_item)
    
    # Create receipt
    db_receipt = PurchaseReceipt(
        **receipt.dict(exclude={'items'}),
        total_amount=total_amount,
        created_by=user_id
    )
    db.add(db_receipt)
    db.flush()  # Get receipt ID
    
    # Add receipt items
    for item in receipt_items:
        item.receipt_id = db_receipt.id
        db.add(item)
    
    # Update order status if all items are received
    if total_amount >= order.total_amount:
        order.status = PurchaseOrderStatus.RECEIVED
    
    db.commit()
    db.refresh(db_receipt)
    return db_receipt

def update_purchase_receipt(
    db: Session, receipt_id: int, receipt: PurchaseReceiptUpdate
) -> Optional[PurchaseReceipt]:
    db_receipt = get_purchase_receipt(db, receipt_id)
    if not db_receipt:
        return None
    
    update_data = receipt.dict(exclude={'items'}, exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_receipt, field, value)
    
    # Update items if provided
    if receipt.items:
        # Delete existing items
        db.query(PurchaseReceiptItem).filter(PurchaseReceiptItem.receipt_id == receipt_id).delete()
        
        # Calculate new total
        total_amount = 0
        for item in receipt.items:
            order_item = db.query(PurchaseOrderItem).filter(
                PurchaseOrderItem.id == item.order_item_id
            ).first()
            if not order_item:
                raise ValueError(f"Order item {item.order_item_id} not found")
            
            item_total = item.quantity * item.unit_price
            total_amount += item_total
            
            receipt_item = PurchaseReceiptItem(
                **item.dict(),
                receipt_id=receipt_id,
                total_amount=item_total
            )
            db.add(receipt_item)
        
        db_receipt.total_amount = total_amount
    
    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)
    return db_receipt 