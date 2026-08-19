import { apiClient } from "@/lib/api-client";
import {
  JobListResponse,
  JobDetailsDTO,
  JobDetailsSchema
} from "@/types/job";

export interface JobListParams {
  page?: number;
  page_size?: number;
  search?: string;
  status?: string;
  department?: string;
  location?: string;
  employment_type?: string;
  sort_by?: string;
  sort_order?: string;
}

export class JobService {
  /**
   * Fetches paginated jobs list
   */
  static async listJobs(params: JobListParams): Promise<JobListResponse> {
    const response = await apiClient.get('/api/v1/jobs', { params });
    // In production with PaginatedResponse, we can parse `items` with z.array() if needed,
    // or assume the generic pagination response is valid from the API Client interceptors.
    return response as unknown as JobListResponse;
  }

  /**
   * Fetches core job details
   */
  static async getDetails(id: string): Promise<JobDetailsDTO> {
    const response = await apiClient.get(`/api/v1/jobs/${id}`);
    return JobDetailsSchema.parse(response);
  }

  // Lazy loaded bounded contexts

  static async getCandidates(id: string) {
    return apiClient.get(`/api/v1/jobs/${id}/candidates`);
  }

  static async getMatches(id: string) {
    return apiClient.get(`/api/v1/jobs/${id}/matches`);
  }

  static async getWorkflow(id: string) {
    return apiClient.get(`/api/v1/jobs/${id}/workflow`);
  }

  static async getAnalytics(id: string) {
    return apiClient.get(`/api/v1/jobs/${id}/analytics`);
  }

  static async getFeedback(id: string) {
    return apiClient.get(`/api/v1/jobs/${id}/feedback`);
  }

  static async getDocuments(id: string) {
    return apiClient.get(`/api/v1/jobs/${id}/documents`);
  }

  static async getHistory(id: string) {
    return apiClient.get(`/api/v1/jobs/${id}/history`);
  }
}
