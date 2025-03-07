import React, { useState, useEffect } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Box,
  Grid,
  Typography,
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon, Add as AddIcon } from '@mui/icons-material';
import { api } from '../../../services/api';
import { PurchaseOrder, PurchaseOrderStatus, Supplier } from '../../../types/purchase';

const PurchaseOrdersList: React.FC = () => {
  const [orders, setOrders] = useState<PurchaseOrder[]>([]);
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [open, setOpen] = useState(false);
  const [editingOrder, setEditingOrder] = useState<PurchaseOrder | null>(null);
  const [formData, setFormData] = useState({
    supplier_id: '',
    order_number: '',
    expected_date: '',
    status: PurchaseOrderStatus.DRAFT,
    notes: '',
    items: [{ product_id: '', quantity: 1, unit_price: 0, discount: 0, notes: '' }],
  });

  const fetchOrders = async () => {
    try {
      const response = await api.get('/purchase/orders');
      setOrders(response.data);
    } catch (error) {
      console.error('Error fetching purchase orders:', error);
    }
  };

  const fetchSuppliers = async () => {
    try {
      const response = await api.get('/purchase/suppliers');
      setSuppliers(response.data);
    } catch (error) {
      console.error('Error fetching suppliers:', error);
    }
  };

  useEffect(() => {
    fetchOrders();
    fetchSuppliers();
  }, []);

  const handleOpen = (order?: PurchaseOrder) => {
    if (order) {
      setEditingOrder(order);
      setFormData({
        supplier_id: order.supplier_id.toString(),
        order_number: order.order_number,
        expected_date: new Date(order.expected_date).toISOString().split('T')[0],
        status: order.status,
        notes: order.notes || '',
        items: order.items.map(item => ({
          product_id: item.product_id.toString(),
          quantity: item.quantity,
          unit_price: item.unit_price,
          discount: item.discount,
          notes: item.notes || '',
        })),
      });
    } else {
      setEditingOrder(null);
      setFormData({
        supplier_id: '',
        order_number: '',
        expected_date: '',
        status: PurchaseOrderStatus.DRAFT,
        notes: '',
        items: [{ product_id: '', quantity: 1, unit_price: 0, discount: 0, notes: '' }],
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingOrder(null);
  };

  const handleSubmit = async () => {
    try {
      if (editingOrder) {
        await api.put(`/purchase/orders/${editingOrder.id}`, formData);
      } else {
        await api.post('/purchase/orders', formData);
      }
      fetchOrders();
      handleClose();
    } catch (error) {
      console.error('Error saving purchase order:', error);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this purchase order?')) {
      try {
        await api.delete(`/purchase/orders/${id}`);
        fetchOrders();
      } catch (error) {
        console.error('Error deleting purchase order:', error);
      }
    }
  };

  const addOrderItem = () => {
    setFormData({
      ...formData,
      items: [...formData.items, { product_id: '', quantity: 1, unit_price: 0, discount: 0, notes: '' }],
    });
  };

  const removeOrderItem = (index: number) => {
    setFormData({
      ...formData,
      items: formData.items.filter((_, i) => i !== index),
    });
  };

  const updateOrderItem = (index: number, field: string, value: any) => {
    const newItems = [...formData.items];
    newItems[index] = { ...newItems[index], [field]: value };
    setFormData({ ...formData, items: newItems });
  };

  return (
    <Box>
      <Box sx={{ mb: 2, display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={() => handleOpen()}
        >
          Add Purchase Order
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Order Number</TableCell>
              <TableCell>Supplier</TableCell>
              <TableCell>Expected Date</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Total Amount</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {orders.map((order) => (
              <TableRow key={order.id}>
                <TableCell>{order.order_number}</TableCell>
                <TableCell>{suppliers.find(s => s.id === order.supplier_id)?.name}</TableCell>
                <TableCell>{new Date(order.expected_date).toLocaleDateString()}</TableCell>
                <TableCell>{order.status}</TableCell>
                <TableCell>${order.total_amount.toFixed(2)}</TableCell>
                <TableCell>
                  <IconButton onClick={() => handleOpen(order)}>
                    <EditIcon />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(order.id)}>
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
        <DialogTitle>{editingOrder ? 'Edit Purchase Order' : 'Add Purchase Order'}</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField
                  select
                  label="Supplier"
                  value={formData.supplier_id}
                  onChange={(e) => setFormData({ ...formData, supplier_id: e.target.value })}
                  fullWidth
                  required
                >
                  {suppliers.map((supplier) => (
                    <MenuItem key={supplier.id} value={supplier.id}>
                      {supplier.name}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  label="Order Number"
                  value={formData.order_number}
                  onChange={(e) => setFormData({ ...formData, order_number: e.target.value })}
                  fullWidth
                  required
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  label="Expected Date"
                  type="date"
                  value={formData.expected_date}
                  onChange={(e) => setFormData({ ...formData, expected_date: e.target.value })}
                  fullWidth
                  required
                  InputLabelProps={{ shrink: true }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  select
                  label="Status"
                  value={formData.status}
                  onChange={(e) => setFormData({ ...formData, status: e.target.value as PurchaseOrderStatus })}
                  fullWidth
                  required
                >
                  {Object.values(PurchaseOrderStatus).map((status) => (
                    <MenuItem key={status} value={status}>
                      {status}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
            </Grid>

            <Typography variant="h6" sx={{ mt: 2 }}>Order Items</Typography>
            {formData.items.map((item, index) => (
              <Box key={index} sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
                <TextField
                  label="Product ID"
                  value={item.product_id}
                  onChange={(e) => updateOrderItem(index, 'product_id', e.target.value)}
                  sx={{ flex: 1 }}
                />
                <TextField
                  label="Quantity"
                  type="number"
                  value={item.quantity}
                  onChange={(e) => updateOrderItem(index, 'quantity', parseInt(e.target.value))}
                  sx={{ flex: 1 }}
                />
                <TextField
                  label="Unit Price"
                  type="number"
                  value={item.unit_price}
                  onChange={(e) => updateOrderItem(index, 'unit_price', parseFloat(e.target.value))}
                  sx={{ flex: 1 }}
                />
                <TextField
                  label="Discount"
                  type="number"
                  value={item.discount}
                  onChange={(e) => updateOrderItem(index, 'discount', parseFloat(e.target.value))}
                  sx={{ flex: 1 }}
                />
                <IconButton onClick={() => removeOrderItem(index)} color="error">
                  <DeleteIcon />
                </IconButton>
              </Box>
            ))}
            <Button
              variant="outlined"
              onClick={addOrderItem}
              startIcon={<AddIcon />}
              sx={{ mt: 1 }}
            >
              Add Item
            </Button>

            <TextField
              label="Notes"
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
              fullWidth
              multiline
              rows={3}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained" color="primary">
            {editingOrder ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PurchaseOrdersList; 