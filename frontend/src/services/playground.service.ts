import { apiClient } from "@/lib/api-client";

export interface PlaygroundExtraction {
  id: string;
  document_id: string;
  provider: string;
  model_name: string;
  prompt_version: string;
  schema_version: string;
  raw_ai_response: any;
  normalized_response: any;
  overall_confidence?: number;
  input_tokens?: number;
  output_tokens?: number;
  total_tokens?: number;
  processing_time_ms?: number;
}

export interface PlaygroundEmbedding {
  id: string;
  embedding_type: string;
  embedding_model: string;
  vector_preview: number[];
  dimensions: number;
}

export interface PlaygroundEvaluation {
  id: string;
  job_requirement_id: string;
  final_score: number;
}

export const playgroundService = {
  getExtractionByDocument: async (documentId: string): Promise<PlaygroundExtraction> => {
    return apiClient.get(`/api/v1/extractions/by-document/${documentId}`);
  },

  getDocument: async (documentId: string): Promise<any> => {
    return apiClient.get(`/api/v1/documents/${documentId}`);
  },

  getDocumentStatus: async (documentId: string): Promise<any> => {
    return apiClient.get(`/api/v1/documents/${documentId}/status`);
  },

  getEmbeddingsByCandidate: async (candidateId: string): Promise<PlaygroundEmbedding[]> => {
    return apiClient.get(`/api/v1/candidates/${candidateId}/embeddings`);
  },

  getEvaluationByCandidate: async (candidateId: string): Promise<PlaygroundEvaluation[]> => {
    return apiClient.get(`/api/v1/candidates/${candidateId}/evaluation`);
  }
};
