import { apiClient } from "@/lib/api-client";
import { 
  AnalyticsResponse, 
  RecruitingFunnelData, 
  MatchingAnalyticsData, 
  WorkflowAnalyticsData, 
  MemoryAnalyticsData, 
  AgentAnalyticsData, 
  ToolAnalyticsData, 
  OrganizationAnalyticsData, 
  PlatformHealthData 
} from "@/types/analytics";

export const AnalyticsService = {
  async getFunnel(): Promise<AnalyticsResponse<RecruitingFunnelData>> {
    const { data } = await apiClient.get<AnalyticsResponse<RecruitingFunnelData>>('/api/v1/analytics/funnel');
    return data;
  },

  async getMatching(): Promise<AnalyticsResponse<MatchingAnalyticsData>> {
    const { data } = await apiClient.get<AnalyticsResponse<MatchingAnalyticsData>>('/api/v1/analytics/matching');
    return data;
  },

  async getWorkflow(): Promise<AnalyticsResponse<WorkflowAnalyticsData>> {
    const { data } = await apiClient.get<AnalyticsResponse<WorkflowAnalyticsData>>('/api/v1/analytics/workflow');
    return data;
  },

  async getMemory(): Promise<AnalyticsResponse<MemoryAnalyticsData>> {
    const { data } = await apiClient.get<AnalyticsResponse<MemoryAnalyticsData>>('/api/v1/analytics/memory');
    return data;
  },

  async getAgent(): Promise<AnalyticsResponse<AgentAnalyticsData>> {
    const { data } = await apiClient.get<AnalyticsResponse<AgentAnalyticsData>>('/api/v1/analytics/agent');
    return data;
  },

  async getTools(): Promise<AnalyticsResponse<ToolAnalyticsData>> {
    const { data } = await apiClient.get<AnalyticsResponse<ToolAnalyticsData>>('/api/v1/analytics/tools');
    return data;
  },

  async getOrganization(): Promise<AnalyticsResponse<OrganizationAnalyticsData>> {
    const { data } = await apiClient.get<AnalyticsResponse<OrganizationAnalyticsData>>('/api/v1/analytics/organization');
    return data;
  },

  async getHealth(): Promise<AnalyticsResponse<PlatformHealthData>> {
    const { data } = await apiClient.get<AnalyticsResponse<PlatformHealthData>>('/api/v1/analytics/health');
    return data;
  }
};
