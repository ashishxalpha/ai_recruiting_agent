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

  // Request Interceptor
  client.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
      // Add correlation ID or auth tokens here if needed
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Response Interceptor
  client.interceptors.response.use(
    (response: AxiosResponse) => {
      return response.data;
    },
    (error: AxiosError) => {
      if (error.response) {
        const status = error.response.status;
        const data: any = error.response.data;
        const message = data?.detail || data?.message || error.message;

        if (status === 401) {
          toast.error("Session expired. Please log in again.");
        } else if (status >= 500) {
          toast.error("An internal server error occurred.");
        }

        return Promise.reject(new ApiError(message, status, data));
      } else if (error.request) {
        toast.error("Network error. Please check your connection.");
        return Promise.reject(new ApiError('No response received from server', 0));
      } else {
        return Promise.reject(new ApiError(error.message));
      }
    }
  );

  return client;
};

export const apiClient = createApiClient();
