import axios from 'axios';

export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor for handling errors globally (e.g. throwing custom errors or handling auth)
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    // We can dispatch toast notifications here if desired, or let the hooks handle it.
    console.error('API Error:', error?.response?.data || error.message);
    return Promise.reject(error);
  }
);
