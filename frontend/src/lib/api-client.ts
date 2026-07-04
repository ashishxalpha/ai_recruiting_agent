import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig, AxiosResponse } from 'axios';
import { toast } from 'sonner';

export class ApiError extends Error {
  public status?: number;
  public data?: any;

  constructor(message: string, status?: number, data?: any) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

const createApiClient = (): AxiosInstance => {
  const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  
  const client = axios.create({
    baseURL,
    timeout: 30000,
    withCredentials: true,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  let isRefreshing = false;
  let failedQueue: any[] = [];

  const processQueue = (error: any, token: string | null = null) => {
    failedQueue.forEach(prom => {
      if (error) {
        prom.reject(error);
      } else {
        prom.resolve(token);
      }
    });
    failedQueue = [];
  };

  client.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
      return config;
    },
    (error) => Promise.reject(error)
  );

  client.interceptors.response.use(
    (response: AxiosResponse) => response.data,
    async (error: AxiosError) => {
      const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

      if (error.response?.status === 401 && !originalRequest._retry) {
        if (isRefreshing) {
          return new Promise(function(resolve, reject) {
            failedQueue.push({ resolve, reject });
          }).then(token => {
            return client(originalRequest);
          }).catch(err => {
            return Promise.reject(err);
          });
        }

        originalRequest._retry = true;
        isRefreshing = true;

        try {
          // Attempt refresh
          await axios.post(`${baseURL}/api/v1/auth/refresh`, {}, { withCredentials: true });
          isRefreshing = false;
          processQueue(null, 'refreshed');
          return client(originalRequest);
        } catch (err) {
          isRefreshing = false;
          processQueue(err, null);
          // Redirect to login or dispatch logout event
          if (typeof window !== 'undefined' && !window.location.pathname.includes('/login')) {
             window.location.href = '/login';
          }
          return Promise.reject(err);
        }
      }

      const status = error.response?.status;
      const data: any = error.response?.data;
      const message = data?.detail || data?.message || error.message;

      if (status === 401) {
        toast.error("Session expired. Please log in again.");
      } else if (status && status >= 500) {
        toast.error("An internal server error occurred.");
      }

      return Promise.reject(new ApiError(message, status, data));
    }
  );

  return client;
};

export const apiClient = createApiClient();
