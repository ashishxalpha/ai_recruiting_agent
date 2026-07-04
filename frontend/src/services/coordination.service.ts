import { apiClient } from "@/lib/api-client";
import { StandardResponse } from "@/types/dashboard";
import {
  CoordinationSession,
  CoordinationConsensus,
  CoordinationHandoff,
  CoordinationConflict
} from "@/types/coordination";

export const CoordinationService = {
  async getOverview(): Promise<StandardResponse<any[]>> {
    const { data } = await apiClient.get<StandardResponse<any[]>>(`/api/v1/coordinator`);
    return data;
  },

  async getSessions(): Promise<StandardResponse<CoordinationSession[]>> {
    const { data } = await apiClient.get<StandardResponse<CoordinationSession[]>>(`/api/v1/coordinator/sessions`);
    return data;
  },

  async getConsensus(): Promise<StandardResponse<CoordinationConsensus[]>> {
    const { data } = await apiClient.get<StandardResponse<CoordinationConsensus[]>>(`/api/v1/coordinator/consensus`);
    return data;
  },

  async getHandoffs(): Promise<StandardResponse<CoordinationHandoff[]>> {
    const { data } = await apiClient.get<StandardResponse<CoordinationHandoff[]>>(`/api/v1/coordinator/handoffs`);
    return data;
  },

  async getConflicts(): Promise<StandardResponse<CoordinationConflict[]>> {
    const { data } = await apiClient.get<StandardResponse<CoordinationConflict[]>>(`/api/v1/coordinator/conflicts`);
    return data;
  }
};
