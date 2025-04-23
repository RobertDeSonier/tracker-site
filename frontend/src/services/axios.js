// axios.js - Axios configuration for API calls
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // Update this URL to match your backend API
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add authorization token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a function to refresh the token
export const refreshToken = async () => {
  try {
    const refresh = localStorage.getItem('refreshToken');
    if (refresh) {
      const response = await apiClient.post('/token/refresh/', { refresh });
      localStorage.setItem('authToken', response.data.access);
      return response.data.access;
    }
  } catch (error) {
    console.error('Failed to refresh token:', error);
    throw error;
  }
};

// Add a response interceptor to handle token refreshing
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const newToken = await refreshToken();
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError);
        localStorage.removeItem('authToken');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Add Axios functions for backend API endpoints

// User Authentication
export const registerUser = (userData) => apiClient.post('/register/', userData);
export const loginUser = (credentials) => apiClient.post('/login/', credentials);
export const logoutUser = () => apiClient.post('/logout/');

// User Profile
export const viewProfile = () => apiClient.get('/view_profile/');
export const updateProfile = (profileData) => apiClient.put('/update_profile/', profileData);

// Items
export const createItem = (itemData) => apiClient.post('/create_item/', itemData);
export const listItems = () => apiClient.get('/list_items/');
export const updateItem = (itemId, itemData) => apiClient.put(`/update_item/${itemId}/`, itemData);
export const deleteItem = (itemId) => apiClient.delete(`/delete_item/${itemId}/`);

// Records
export const createRecord = (recordData) => apiClient.post('/create_record/', recordData);
export const listRecords = (itemId) => apiClient.get(`/list_records/${itemId}/`);
export const updateRecord = (recordId, recordData) => apiClient.put(`/update_record/${recordId}/`, recordData);
export const deleteRecord = (recordId) => apiClient.delete(`/delete_record/${recordId}/`);

export default apiClient;