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
import { PurchaseReceipt, ReceiptStatus, PurchaseOrder } from '../../../types/purchase';

const PurchaseReceiptsList: React.FC = () => {
  const [receipts, setReceipts] = useState<PurchaseReceipt[]>([]);
  const [orders, setOrders] = useState<PurchaseOrder[]>([]);
  const [open, setOpen] = useState(false);
  const [editingReceipt, setEditingReceipt] = useState<PurchaseReceipt | null>(null);
  const [formData, setFormData] = useState({
    order_id: '',
    receipt_number: '',
    status: ReceiptStatus.DRAFT,
    notes: '',
    items: [{ order_item_id: '', quantity: 1, unit_price: 0, notes: '' }],
  });

  const fetchReceipts = async () => {
    try {
      const response = await api.get('/purchase/receipts');
      setReceipts(response.data);
    } catch (error) {
      console.error('Error fetching purchase receipts:', error);
    }
  };

  const fetchOrders = async () => {
    try {
      const response = await api.get('/purchase/orders');
      setOrders(response.data);
    } catch (error) {
      console.error('Error fetching purchase orders:', error);
    }
  };

  useEffect(() => {
    fetchReceipts();
    fetchOrders();
  }, []);

  const handleOpen = (receipt?: PurchaseReceipt) => {
    if (receipt) {
      setEditingReceipt(receipt);
      setFormData({
        order_id: receipt.order_id.toString(),
        receipt_number: receipt.receipt_number,
        status: receipt.status,
        notes: receipt.notes || '',
        items: receipt.items.map(item => ({
          order_item_id: item.order_item_id.toString(),
          quantity: item.quantity,
          unit_price: item.unit_price,
          notes: item.notes || '',
        })),
      });
    } else {
      setEditingReceipt(null);
      setFormData({
        order_id: '',
        receipt_number: '',
        status: ReceiptStatus.DRAFT,
        notes: '',
        items: [{ order_item_id: '', quantity: 1, unit_price: 0, notes: '' }],
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingReceipt(null);
  };

  const handleSubmit = async () => {
    try {
      if (editingReceipt) {
        await api.put(`/purchase/receipts/${editingReceipt.id}`, formData);
      } else {
        await api.post('/purchase/receipts', formData);
      }
      fetchReceipts();
      handleClose();
    } catch (error) {
      console.error('Error saving purchase receipt:', error);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this purchase receipt?')) {
      try {
        await api.delete(`/purchase/receipts/${id}`);
        fetchReceipts();
      } catch (error) {
        console.error('Error deleting purchase receipt:', error);
      }
    }
  };

  const addReceiptItem = () => {
    setFormData({
      ...formData,
      items: [...formData.items, { order_item_id: '', quantity: 1, unit_price: 0, notes: '' }],
    });
  };

  const removeReceiptItem = (index: number) => {
    setFormData({
      ...formData,
      items: formData.items.filter((_, i) => i !== index),
    });
  };

  const updateReceiptItem = (index: number, field: string, value: any) => {
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
          Add Purchase Receipt
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Receipt Number</TableCell>
              <TableCell>Order Number</TableCell>
              <TableCell>Date</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Total Amount</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {receipts.map((receipt) => (
              <TableRow key={receipt.id}>
                <TableCell>{receipt.receipt_number}</TableCell>
                <TableCell>{orders.find(o => o.id === receipt.order_id)?.order_number}</TableCell>
                <TableCell>{new Date(receipt.receipt_date).toLocaleDateString()}</TableCell>
                <TableCell>{receipt.status}</TableCell>
                <TableCell>${receipt.total_amount.toFixed(2)}</TableCell>
                <TableCell>
                  <IconButton onClick={() => handleOpen(receipt)}>
                    <EditIcon />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(receipt.id)}>
                    <DeleteIcon />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
        <DialogTitle>{editingReceipt ? 'Edit Purchase Receipt' : 'Add Purchase Receipt'}</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField
                  select
                  label="Purchase Order"
                  value={formData.order_id}
                  onChange={(e) => setFormData({ ...formData, order_id: e.target.value })}
                  fullWidth
                  required
                >
                  {orders.map((order) => (
                    <MenuItem key={order.id} value={order.id}>
                      {order.order_number}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  label="Receipt Number"
                  value={formData.receipt_number}
                  onChange={(e) => setFormData({ ...formData, receipt_number: e.target.value })}
                  fullWidth
                  required
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  select
                  label="Status"
                  value={formData.status}
                  onChange={(e) => setFormData({ ...formData, status: e.target.value as ReceiptStatus })}
                  fullWidth
                  required
                >
                  {Object.values(ReceiptStatus).map((status) => (
                    <MenuItem key={status} value={status}>
                      {status}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
            </Grid>

            <Typography variant="h6" sx={{ mt: 2 }}>Receipt Items</Typography>
            {formData.items.map((item, index) => (
              <Box key={index} sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
                <TextField
                  label="Order Item ID"
                  value={item.order_item_id}
                  onChange={(e) => updateReceiptItem(index, 'order_item_id', e.target.value)}
                  sx={{ flex: 1 }}
                />
                <TextField
                  label="Quantity"
                  type="number"
                  value={item.quantity}
                  onChange={(e) => updateReceiptItem(index, 'quantity', parseInt(e.target.value))}
                  sx={{ flex: 1 }}
                />
                <TextField
                  label="Unit Price"
                  type="number"
                  value={item.unit_price}
                  onChange={(e) => updateReceiptItem(index, 'unit_price', parseFloat(e.target.value))}
                  sx={{ flex: 1 }}
                />
                <IconButton onClick={() => removeReceiptItem(index)} color="error">
                  <DeleteIcon />
                </IconButton>
              </Box>
            ))}
            <Button
              variant="outlined"
              onClick={addReceiptItem}
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
            {editingReceipt ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PurchaseReceiptsList; 