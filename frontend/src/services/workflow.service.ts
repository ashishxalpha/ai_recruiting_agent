import { apiClient } from "@/lib/api-client";
import { 
  WorkflowResponse,
  WorkflowSummaryData,
  WorkflowTimelineData,
  WorkflowGraphData,
  WorkflowNodeHistoryData,
  WorkflowEventListData,
  WorkflowCheckpointListData,
  WorkflowStatisticsData
} from "@/types/workflow";

export const WorkflowService = {
  async getSummary(id: string): Promise<WorkflowResponse<WorkflowSummaryData>> {
    const response = await apiClient.get<any, WorkflowResponse<WorkflowSummaryData>>(`/api/v1/workflows/${id}`);
    return response;
  },

  async getTimeline(id: string): Promise<WorkflowResponse<WorkflowTimelineData>> {
    const response = await apiClient.get<any, WorkflowResponse<WorkflowTimelineData>>(`/api/v1/workflows/${id}/timeline`);
    return response;
  },

  async getGraph(id: string): Promise<WorkflowResponse<WorkflowGraphData>> {
    const response = await apiClient.get<any, WorkflowResponse<WorkflowGraphData>>(`/api/v1/workflows/${id}/graph`);
    return response;
  },

  async getNodes(id: string): Promise<WorkflowResponse<WorkflowNodeHistoryData>> {
    const response = await apiClient.get<any, WorkflowResponse<WorkflowNodeHistoryData>>(`/api/v1/workflows/${id}/nodes`);
    return response;
  },

  async getEvents(id: string): Promise<WorkflowResponse<WorkflowEventListData>> {
    const response = await apiClient.get<any, WorkflowResponse<WorkflowEventListData>>(`/api/v1/workflows/${id}/events`);
    return response;
  },

  async getCheckpoints(id: string): Promise<WorkflowResponse<WorkflowCheckpointListData>> {
    const response = await apiClient.get<any, WorkflowResponse<WorkflowCheckpointListData>>(`/api/v1/workflows/${id}/checkpoints`);
    return response;
  },

  async getStatistics(id: string): Promise<WorkflowResponse<WorkflowStatisticsData>> {
    const response = await apiClient.get<any, WorkflowResponse<WorkflowStatisticsData>>(`/api/v1/workflows/${id}/statistics`);
    return response;
  }
};
