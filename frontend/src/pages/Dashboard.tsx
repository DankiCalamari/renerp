import React from 'react';
import { Grid, Paper, Typography } from '@mui/material';
import {
  Inventory as InventoryIcon,
  ShoppingCart as SalesIcon,
  LocalShipping as PurchaseIcon,
} from '@mui/icons-material';

const Dashboard: React.FC = () => {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
      </Grid>
      <Grid item xs={12} md={4}>
        <Paper
          sx={{
            p: 2,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            height: 140,
          }}
        >
          <InventoryIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
          <Typography variant="h6">Inventory Management</Typography>
          <Typography variant="body2" color="text.secondary">
            Manage your products and stock levels
          </Typography>
        </Paper>
      </Grid>
      <Grid item xs={12} md={4}>
        <Paper
          sx={{
            p: 2,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            height: 140,
          }}
        >
          <SalesIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
          <Typography variant="h6">Sales Management</Typography>
          <Typography variant="body2" color="text.secondary">
            Track sales and manage orders
          </Typography>
        </Paper>
      </Grid>
      <Grid item xs={12} md={4}>
        <Paper
          sx={{
            p: 2,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            height: 140,
          }}
        >
          <PurchaseIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
          <Typography variant="h6">Purchase Management</Typography>
          <Typography variant="body2" color="text.secondary">
            Manage suppliers and purchase orders
          </Typography>
        </Paper>
      </Grid>
    </Grid>
  );
};

export default Dashboard; 