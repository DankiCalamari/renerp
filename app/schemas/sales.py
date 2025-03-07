from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.sales import CustomerType, OrderStatus, PaymentStatus

# Customer schemas
class CustomerBase(BaseModel):
    name: str
    type: CustomerType
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    credit_limit: float = 0.0
    is_active: bool = True

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    type: Optional[CustomerType] = None
    credit_limit: Optional[float] = None
    is_active: Optional[bool] = None

class Customer(CustomerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Order Item schemas
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    discount: float = 0.0
    notes: Optional[str] = None

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    total_amount: float

    class Config:
        from_attributes = True

# Order schemas
class OrderBase(BaseModel):
    customer_id: int
    order_number: str
    status: OrderStatus = OrderStatus.DRAFT
    notes: Optional[str] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(OrderBase):
    customer_id: Optional[int] = None
    order_number: Optional[str] = None
    status: Optional[OrderStatus] = None
    items: Optional[List[OrderItemCreate]] = None

class Order(OrderBase):
    id: int
    order_date: datetime
    total_amount: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int
    items: List[OrderItem]

    class Config:
        from_attributes = True

# Invoice schemas
class InvoiceBase(BaseModel):
    order_id: int
    invoice_number: str
    due_date: datetime
    total_amount: float
    tax_amount: float
    payment_status: PaymentStatus = PaymentStatus.PENDING
    notes: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(InvoiceBase):
    order_id: Optional[int] = None
    invoice_number: Optional[str] = None
    due_date: Optional[datetime] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    payment_status: Optional[PaymentStatus] = None

class Invoice(InvoiceBase):
    id: int
    invoice_date: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: int

    class Config:
        from_attributes = True

# Payment schemas
class PaymentBase(BaseModel):
    invoice_id: int
    amount: float
    payment_method: str
    reference: Optional[str] = None
    notes: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    payment_date: datetime
    created_at: datetime
    created_by: int

    class Config:
        from_attributes = True 