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
    const { data } = await apiClient.get<MemoryResponse<MemoryList>>(`/api/v1/memory`);
    return data;
  },

  async getDetails(id: string): Promise<MemoryResponse<MemoryDetails>> {
    const { data } = await apiClient.get<MemoryResponse<MemoryDetails>>(`/api/v1/memory/${id}`);
    return data;
  },

  async search(query: string, filters?: Record<string, any>): Promise<MemoryResponse<MemoryRetrieval>> {
    const { data } = await apiClient.post<MemoryResponse<MemoryRetrieval>>(`/api/v1/memory/search`, {
      query,
      filters
    });
    return data;
  },

  async getGraph(): Promise<MemoryResponse<MemoryGraphData>> {
    const { data } = await apiClient.get<MemoryResponse<MemoryGraphData>>(`/api/v1/memory/graph`);
    return data;
  },

  async getTimeline(id: string): Promise<MemoryResponse<MemoryTimelineData>> {
    const { data } = await apiClient.get<MemoryResponse<MemoryTimelineData>>(`/api/v1/memory/${id}/timeline`);
    return data;
  },

  async getRelationships(id: string): Promise<MemoryResponse<MemoryRelationshipListData>> {
    const { data } = await apiClient.get<MemoryResponse<MemoryRelationshipListData>>(`/api/v1/memory/${id}/relationships`);
    return data;
  },

  async getConsolidations(): Promise<MemoryResponse<MemoryConsolidationData>> {
    const { data } = await apiClient.get<MemoryResponse<MemoryConsolidationData>>(`/api/v1/memory/consolidations`);
    return data;
  },

  async getStatistics(): Promise<MemoryResponse<MemoryStatistics>> {
    const { data } = await apiClient.get<MemoryResponse<MemoryStatistics>>(`/api/v1/memory/statistics`);
    return data;
  }
};
