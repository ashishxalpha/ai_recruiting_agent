import { apiClient } from "@/lib/api-client";
import { 
  CandidateListResponse, 
  CandidateDetailsDTO, 
  CandidateDetailsSchema 
} from "@/types/candidate";

export interface CandidateListParams {
  page?: number;
  page_size?: number;
  search?: string;
  status?: string;
  sort_by?: string;
  sort_order?: string;
}

export class CandidateService {
  /**
   * Fetches paginated candidates list
   */
  static async listCandidates(params: CandidateListParams): Promise<CandidateListResponse> {
    const response = await apiClient.get('/candidates', { params });
    // In production with PaginatedResponse, we can parse `items` with z.array() if needed,
    // or assume the generic pagination response is valid.
    return response as CandidateListResponse;
  }

  /**
   * Fetches core candidate details (profile, skills, experience, education, projects)
   */
  static async getDetails(id: string): Promise<CandidateDetailsDTO> {
    const response = await apiClient.get(`/candidates/${id}`);
    return CandidateDetailsSchema.parse(response);
  }

  // Lazy loaded bounded contexts
  
  static async getWorkflow(id: string) {
    return apiClient.get(`/candidates/${id}/workflow`);
  }

  static async getEvaluation(id: string) {
    return apiClient.get(`/candidates/${id}/evaluation`);
  }

  static async getEmbeddings(id: string) {
    return apiClient.get(`/candidates/${id}/embeddings`);
  }

  static async getMemory(id: string) {
    return apiClient.get(`/candidates/${id}/memory`);
  }

  static async getMatches(id: string) {
    return apiClient.get(`/candidates/${id}/matches`);
  }

  static async getFeedback(id: string) {
    return apiClient.get(`/candidates/${id}/feedback`);
  }

  static async getDocuments(id: string) {
    return apiClient.get(`/candidates/${id}/documents`);
  }
}
