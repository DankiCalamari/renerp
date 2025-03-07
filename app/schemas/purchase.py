from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.purchase import SupplierType, PurchaseOrderStatus, ReceiptStatus

# Supplier schemas
class SupplierBase(BaseModel):
    name: str
    type: SupplierType
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    payment_terms: Optional[int] = None
    is_active: bool = True

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(SupplierBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    type: Optional[SupplierType] = None
    payment_terms: Optional[int] = None
    is_active: Optional[bool] = None

class Supplier(SupplierBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Purchase Order Item schemas
class PurchaseOrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    discount: float = 0.0
    notes: Optional[str] = None

class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    pass

class PurchaseOrderItem(PurchaseOrderItemBase):
    id: int
    order_id: int
    total_amount: float

    class Config:
        from_attributes = True

# Purchase Order schemas
class PurchaseOrderBase(BaseModel):
    supplier_id: int
    order_number: str
    expected_date: datetime
    status: PurchaseOrderStatus = PurchaseOrderStatus.DRAFT
    notes: Optional[str] = None

class PurchaseOrderCreate(PurchaseOrderBase):
    items: List[PurchaseOrderItemCreate]

class PurchaseOrderUpdate(PurchaseOrderBase):
    supplier_id: Optional[int] = None
    order_number: Optional[str] = None
    expected_date: Optional[datetime] = None
    status: Optional[PurchaseOrderStatus] = None
    items: Optional[List[PurchaseOrderItemCreate]] = None

class PurchaseOrder(PurchaseOrderBase):
    id: int
    order_date: datetime
    total_amount: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    items: List[PurchaseOrderItem]

    class Config:
        from_attributes = True

# Purchase Receipt Item schemas
class PurchaseReceiptItemBase(BaseModel):
    order_item_id: int
    quantity: int
    unit_price: float
    notes: Optional[str] = None

class PurchaseReceiptItemCreate(PurchaseReceiptItemBase):
    pass

class PurchaseReceiptItem(PurchaseReceiptItemBase):
    id: int
    receipt_id: int
    total_amount: float

    class Config:
        from_attributes = True

# Purchase Receipt schemas
class PurchaseReceiptBase(BaseModel):
    order_id: int
    receipt_number: str
    status: ReceiptStatus = ReceiptStatus.DRAFT
    notes: Optional[str] = None

class PurchaseReceiptCreate(PurchaseReceiptBase):
    items: List[PurchaseReceiptItemCreate]

class PurchaseReceiptUpdate(PurchaseReceiptBase):
    order_id: Optional[int] = None
    receipt_number: Optional[str] = None
    status: Optional[ReceiptStatus] = None
    items: Optional[List[PurchaseReceiptItemCreate]] = None

class PurchaseReceipt(PurchaseReceiptBase):
    id: int
    receipt_date: datetime
    total_amount: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    items: List[PurchaseReceiptItem]

    class Config:
        from_attributes = True 