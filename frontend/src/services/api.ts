import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for handling cookies
});

// Request interceptor for API calls
api.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${token}`,
      };
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor for API calls
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config;

    // Handle 401 Unauthorized errors
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
      return Promise.reject(error);
    }

    // Handle 403 Forbidden errors
    if (error.response?.status === 403) {
      // You might want to show a message to the user
      console.error('Access forbidden');
      return Promise.reject(error);
    }

    // Handle 404 Not Found errors
    if (error.response?.status === 404) {
      console.error('Resource not found');
      return Promise.reject(error);
    }

    // Handle 500 Internal Server errors
    if (error.response?.status === 500) {
      console.error('Internal server error');
      return Promise.reject(error);
    }

    return Promise.reject(error);
  }
);

// API endpoints
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  logout: () => api.post('/auth/logout'),
  refreshToken: () => api.post('/auth/refresh-token'),
};

export const purchaseAPI = {
  // Supplier endpoints
  getSuppliers: () => api.get('/purchase/suppliers'),
  getSupplier: (id: number) => api.get(`/purchase/suppliers/${id}`),
  createSupplier: (data: any) => api.post('/purchase/suppliers', data),
  updateSupplier: (id: number, data: any) => api.put(`/purchase/suppliers/${id}`, data),
  deleteSupplier: (id: number) => api.delete(`/purchase/suppliers/${id}`),

  // Purchase Order endpoints
  getPurchaseOrders: () => api.get('/purchase/orders'),
  getPurchaseOrder: (id: number) => api.get(`/purchase/orders/${id}`),
  createPurchaseOrder: (data: any) => api.post('/purchase/orders', data),
  updatePurchaseOrder: (id: number, data: any) => api.put(`/purchase/orders/${id}`, data),
  deletePurchaseOrder: (id: number) => api.delete(`/purchase/orders/${id}`),

  // Purchase Receipt endpoints
  getPurchaseReceipts: () => api.get('/purchase/receipts'),
  getPurchaseReceipt: (id: number) => api.get(`/purchase/receipts/${id}`),
  createPurchaseReceipt: (data: any) => api.post('/purchase/receipts', data),
  updatePurchaseReceipt: (id: number, data: any) => api.put(`/purchase/receipts/${id}`, data),
  deletePurchaseReceipt: (id: number) => api.delete(`/purchase/receipts/${id}`),
};

export const inventoryAPI = {
  getProducts: () => api.get('/inventory/products'),
  getProduct: (id: number) => api.get(`/inventory/products/${id}`),
  createProduct: (data: any) => api.post('/inventory/products', data),
  updateProduct: (id: number, data: any) => api.put(`/inventory/products/${id}`, data),
  deleteProduct: (id: number) => api.delete(`/inventory/products/${id}`),
};

export const salesAPI = {
  getSalesOrders: () => api.get('/sales/orders'),
  getSalesOrder: (id: number) => api.get(`/sales/orders/${id}`),
  createSalesOrder: (data: any) => api.post('/sales/orders', data),
  updateSalesOrder: (id: number, data: any) => api.put(`/sales/orders/${id}`, data),
  deleteSalesOrder: (id: number) => api.delete(`/sales/orders/${id}`),
};

export default api; 