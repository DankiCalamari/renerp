import React from 'react';
import { Box, Container, Grid, Paper, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import PurchaseOrdersList from './components/PurchaseOrdersList';
import SuppliersList from './components/SuppliersList';
import PurchaseReceiptsList from './components/PurchaseReceiptsList';

const PurchaseManagement: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Header */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography component="h1" variant="h4" color="primary" gutterBottom>
              Purchase Management
            </Typography>
          </Paper>
        </Grid>

        {/* Purchase Orders Section */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Purchase Orders
            </Typography>
            <PurchaseOrdersList />
          </Paper>
        </Grid>

        {/* Suppliers Section */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Suppliers
            </Typography>
            <SuppliersList />
          </Paper>
        </Grid>

        {/* Purchase Receipts Section */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Purchase Receipts
            </Typography>
            <PurchaseReceiptsList />
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default PurchaseManagement; 