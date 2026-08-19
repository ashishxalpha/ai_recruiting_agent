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
    const response = await apiClient.get<any, StandardResponse<any[]>>(`/api/v1/coordinator`);
    return response;
  },

  async getSessions(): Promise<StandardResponse<CoordinationSession[]>> {
    const response = await apiClient.get<any, StandardResponse<CoordinationSession[]>>(`/api/v1/coordinator/sessions`);
    return response;
  },

  async getConsensus(): Promise<StandardResponse<CoordinationConsensus[]>> {
    const response = await apiClient.get<any, StandardResponse<CoordinationConsensus[]>>(`/api/v1/coordinator/consensus`);
    return response;
  },

  async getHandoffs(): Promise<StandardResponse<CoordinationHandoff[]>> {
    const response = await apiClient.get<any, StandardResponse<CoordinationHandoff[]>>(`/api/v1/coordinator/handoffs`);
    return response;
  },

  async getConflicts(): Promise<StandardResponse<CoordinationConflict[]>> {
    const response = await apiClient.get<any, StandardResponse<CoordinationConflict[]>>(`/api/v1/coordinator/conflicts`);
    return response;
  }
};
