import { apiClient } from "@/lib/api-client";
import { 
  MemoryResponse,
  MemoryList,
  MemoryDetails,
  MemoryRetrieval,
  MemoryGraphData,
  MemoryTimelineData,
  MemoryRelationshipListData,
  MemoryConsolidationData,
  MemoryStatistics
} from "@/types/memory";

export const MemoryService = {
  async list(): Promise<MemoryResponse<MemoryList>> {
    const response = await apiClient.get<any, MemoryResponse<MemoryList>>(`/api/v1/memory`);
    return response;
  },

  async getDetails(id: string): Promise<MemoryResponse<MemoryDetails>> {
    const response = await apiClient.get<any, MemoryResponse<MemoryDetails>>(`/api/v1/memory/${id}`);
    return response;
  },

  async search(query: string, filters?: Record<string, any>): Promise<MemoryResponse<MemoryRetrieval>> {
    const response = await apiClient.post<any, MemoryResponse<MemoryRetrieval>>(`/api/v1/memory/search`, {
      query,
      filters
    });
    return response;
  },

  async getGraph(): Promise<MemoryResponse<MemoryGraphData>> {
    const response = await apiClient.get<any, MemoryResponse<MemoryGraphData>>(`/api/v1/memory/graph`);
    return response;
  },

  async getTimeline(id: string): Promise<MemoryResponse<MemoryTimelineData>> {
    const response = await apiClient.get<any, MemoryResponse<MemoryTimelineData>>(`/api/v1/memory/${id}/timeline`);
    return response;
  },

  async getRelationships(id: string): Promise<MemoryResponse<MemoryRelationshipListData>> {
    const response = await apiClient.get<any, MemoryResponse<MemoryRelationshipListData>>(`/api/v1/memory/${id}/relationships`);
    return response;
  },

  async getConsolidations(): Promise<MemoryResponse<MemoryConsolidationData>> {
    const response = await apiClient.get<any, MemoryResponse<MemoryConsolidationData>>(`/api/v1/memory/consolidations`);
    return response;
  },

  async getStatistics(): Promise<MemoryResponse<MemoryStatistics>> {
    const response = await apiClient.get<any, MemoryResponse<MemoryStatistics>>(`/api/v1/memory/statistics`);
    return response;
  }
};
