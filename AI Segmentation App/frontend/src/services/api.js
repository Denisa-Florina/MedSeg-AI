import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
});

api.interceptors.request.use(
  (config) => {
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type'];
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const { status, data } = error.response;
      
      console.error('API Error:', {
        status,
        data,
        url: error.config?.url,
        method: error.config?.method
      });
      
      if (status === 401 && window.location.pathname !== '/login') {
        localStorage.removeItem('authToken');
        window.location.href = '/login';
      }
      
      return Promise.reject(new Error(data.error || 'An error occurred'));
    }
    return Promise.reject(new Error('No response from server'));
  }
);

export default api;