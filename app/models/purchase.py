from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base_class import Base

class SupplierType(str, enum.Enum):
    MANUFACTURER = "manufacturer"
    DISTRIBUTOR = "distributor"
    WHOLESALER = "wholesaler"
    RETAILER = "retailer"

class PurchaseOrderStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    CONFIRMED = "confirmed"
    RECEIVED = "received"
    CANCELLED = "cancelled"

class ReceiptStatus(str, enum.Enum):
    DRAFT = "draft"
    RECEIVED = "received"
    CANCELLED = "cancelled"

class Supplier(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(Enum(SupplierType), nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    address = Column(Text)
    tax_id = Column(String)  # VAT/Tax ID
    payment_terms = Column(Integer)  # Days to pay
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")

class PurchaseOrder(Base):
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("supplier.id"), nullable=False)
    order_number = Column(String, unique=True, index=True, nullable=False)
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    expected_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(PurchaseOrderStatus), default=PurchaseOrderStatus.DRAFT)
    total_amount = Column(Float, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("user.id"), nullable=False)

    # Relationships
    supplier = relationship("Supplier", back_populates="purchase_orders")
    items = relationship("PurchaseOrderItem", back_populates="order")
    receipts = relationship("PurchaseReceipt", back_populates="order")
    user = relationship("User")

class PurchaseOrderItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("purchaseorder.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    notes = Column(Text)

    # Relationships
    order = relationship("PurchaseOrder", back_populates="items")
    product = relationship("Product")

class PurchaseReceipt(Base):
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("purchaseorder.id"), nullable=False)
    receipt_number = Column(String, unique=True, index=True, nullable=False)
    receipt_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(ReceiptStatus), default=ReceiptStatus.DRAFT)
    total_amount = Column(Float, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("user.id"), nullable=False)

    # Relationships
    order = relationship("PurchaseOrder", back_populates="receipts")
    items = relationship("PurchaseReceiptItem", back_populates="receipt")
    user = relationship("User")

class PurchaseReceiptItem(Base):
    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(Integer, ForeignKey("purchasereceipt.id"), nullable=False)
    order_item_id = Column(Integer, ForeignKey("purchaseorderitem.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    notes = Column(Text)

    # Relationships
    receipt = relationship("PurchaseReceipt", back_populates="items")
    order_item = relationship("PurchaseOrderItem") 