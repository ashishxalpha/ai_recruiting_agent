import { apiClient } from "@/lib/api-client";
import { 
  StandardResponse,
  DashboardSummary,
  DashboardHealth,
  RecentActivity
} from "@/types/dashboard";

export const DashboardService = {
  async getSummary(): Promise<StandardResponse<DashboardSummary>> {
    const response = await apiClient.get<any, StandardResponse<DashboardSummary>>(`/api/v1/dashboard/summary`);
    return response;
  },

  async getHealth(): Promise<StandardResponse<DashboardHealth>> {
    const response = await apiClient.get<any, StandardResponse<DashboardHealth>>(`/api/v1/dashboard/health`);
    return response;
  },

  async getActivity(limit: number = 20): Promise<StandardResponse<RecentActivity>> {
    const response = await apiClient.get<any, StandardResponse<RecentActivity>>(`/api/v1/dashboard/activity`, {
      params: { limit }
    });
    return response;
  }
};
