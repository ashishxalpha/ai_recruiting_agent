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
    const response = await apiClient.get<any, AnalyticsResponse<RecruitingFunnelData>>('/api/v1/analytics/funnel');
    return response;
  },

  async getMatching(): Promise<AnalyticsResponse<MatchingAnalyticsData>> {
    const response = await apiClient.get<any, AnalyticsResponse<MatchingAnalyticsData>>('/api/v1/analytics/matching');
    return response;
  },

  async getWorkflow(): Promise<AnalyticsResponse<WorkflowAnalyticsData>> {
    const response = await apiClient.get<any, AnalyticsResponse<WorkflowAnalyticsData>>('/api/v1/analytics/workflow');
    return response;
  },

  async getMemory(): Promise<AnalyticsResponse<MemoryAnalyticsData>> {
    const response = await apiClient.get<any, AnalyticsResponse<MemoryAnalyticsData>>('/api/v1/analytics/memory');
    return response;
  },

  async getAgent(): Promise<AnalyticsResponse<AgentAnalyticsData>> {
    const response = await apiClient.get<any, AnalyticsResponse<AgentAnalyticsData>>('/api/v1/analytics/agent');
    return response;
  },

  async getTools(): Promise<AnalyticsResponse<ToolAnalyticsData>> {
    const response = await apiClient.get<any, AnalyticsResponse<ToolAnalyticsData>>('/api/v1/analytics/tools');
    return response;
  },

  async getOrganization(): Promise<AnalyticsResponse<OrganizationAnalyticsData>> {
    const response = await apiClient.get<any, AnalyticsResponse<OrganizationAnalyticsData>>('/api/v1/analytics/organization');
    return response;
  },

  async getHealth(): Promise<AnalyticsResponse<PlatformHealthData>> {
    const response = await apiClient.get<any, AnalyticsResponse<PlatformHealthData>>('/api/v1/analytics/health');
    return response;
  }
};
