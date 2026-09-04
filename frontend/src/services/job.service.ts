import { apiClient } from "@/lib/api-client";
import {
  JobListResponse,
  JobDetailsDTO,
  JobDetailsSchema,
  JobCandidateMatchDTO,
  JobWorkflowDTO,
  JobAnalyticsDTO
} from "@/types/job";
import { CandidateSummaryDTO } from "@/types/candidate";

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

  static async getCandidates(id: string): Promise<CandidateSummaryDTO[]> {
    const response = await apiClient.get(`/api/v1/jobs/${id}/candidates`);
    return response as unknown as CandidateSummaryDTO[];
  }

  static async getMatches(id: string): Promise<JobCandidateMatchDTO[]> {
    const response = await apiClient.get(`/api/v1/jobs/${id}/matches`);
    return response as unknown as JobCandidateMatchDTO[];
  }

  static async getWorkflow(id: string): Promise<JobWorkflowDTO[]> {
    const response = await apiClient.get(`/api/v1/jobs/${id}/workflow`);
    return response as unknown as JobWorkflowDTO[];
  }

  static async getAnalytics(id: string): Promise<JobAnalyticsDTO> {
    const response = await apiClient.get(`/api/v1/jobs/${id}/analytics`);
    return response as unknown as JobAnalyticsDTO;
  }

  static async getFeedback(id: string): Promise<Record<string, unknown>[]> {
    const response = await apiClient.get(`/api/v1/jobs/${id}/feedback`);
    return response as unknown as Record<string, unknown>[];
  }

  static async getDocuments(id: string): Promise<Record<string, unknown>[]> {
    const response = await apiClient.get(`/api/v1/jobs/${id}/documents`);
    return response as unknown as Record<string, unknown>[];
  }

  static async getHistory(id: string): Promise<Record<string, unknown>[]> {
    const response = await apiClient.get(`/api/v1/jobs/${id}/history`);
    return response as unknown as Record<string, unknown>[];
  }
}
