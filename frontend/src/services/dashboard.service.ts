import { apiClient } from "@/lib/api-client";
import { 
  StandardResponse,
  DashboardSummary,
  DashboardHealth,
  RecentActivity
} from "@/types/dashboard";

export const DashboardService = {
  async getSummary(): Promise<StandardResponse<DashboardSummary>> {
    const { data } = await apiClient.get<StandardResponse<DashboardSummary>>(`/api/v1/dashboard/summary`);
    return data;
  },

  async getHealth(): Promise<StandardResponse<DashboardHealth>> {
    const { data } = await apiClient.get<StandardResponse<DashboardHealth>>(`/api/v1/dashboard/health`);
    return data;
  },

  async getActivity(limit: number = 20): Promise<StandardResponse<RecentActivity>> {
    const { data } = await apiClient.get<StandardResponse<RecentActivity>>(`/api/v1/dashboard/activity`, {
      params: { limit }
    });
    return data;
  }
};
