export enum SupplierType {
  MANUFACTURER = 'manufacturer',
  DISTRIBUTOR = 'distributor',
  WHOLESALER = 'wholesaler',
  RETAILER = 'retailer',
}

export enum PurchaseOrderStatus {
  DRAFT = 'draft',
  SENT = 'sent',
  CONFIRMED = 'confirmed',
  RECEIVED = 'received',
  CANCELLED = 'cancelled',
}

export enum ReceiptStatus {
  DRAFT = 'draft',
  RECEIVED = 'received',
  CANCELLED = 'cancelled',
}

export interface Supplier {
  id: number;
  name: string;
  type: SupplierType;
  email: string;
  phone?: string;
  address?: string;
  tax_id?: string;
  payment_terms?: number;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface PurchaseOrderItem {
  id: number;
  order_id: number;
  product_id: number;
  quantity: number;
  unit_price: number;
  discount: number;
  total_amount: number;
  notes?: string;
}

export interface PurchaseOrder {
  id: number;
  supplier_id: number;
  order_number: string;
  order_date: string;
  expected_date: string;
  status: PurchaseOrderStatus;
  total_amount: number;
  notes?: string;
  created_at: string;
  updated_at?: string;
  created_by: number;
  items: PurchaseOrderItem[];
}

export interface PurchaseReceiptItem {
  id: number;
  receipt_id: number;
  order_item_id: number;
  quantity: number;
  unit_price: number;
  total_amount: number;
  notes?: string;
}

export interface PurchaseReceipt {
  id: number;
  order_id: number;
  receipt_number: string;
  receipt_date: string;
  status: ReceiptStatus;
  total_amount: number;
  notes?: string;
  created_at: string;
  updated_at?: string;
  created_by: number;
  items: PurchaseReceiptItem[];
} 