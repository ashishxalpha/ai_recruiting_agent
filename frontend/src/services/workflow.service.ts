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
    const { data } = await apiClient.get<WorkflowResponse<WorkflowSummaryData>>(`/api/v1/workflows/${id}`);
    return data;
  },

  async getTimeline(id: string): Promise<WorkflowResponse<WorkflowTimelineData>> {
    const { data } = await apiClient.get<WorkflowResponse<WorkflowTimelineData>>(`/api/v1/workflows/${id}/timeline`);
    return data;
  },

  async getGraph(id: string): Promise<WorkflowResponse<WorkflowGraphData>> {
    const { data } = await apiClient.get<WorkflowResponse<WorkflowGraphData>>(`/api/v1/workflows/${id}/graph`);
    return data;
  },

  async getNodes(id: string): Promise<WorkflowResponse<WorkflowNodeHistoryData>> {
    const { data } = await apiClient.get<WorkflowResponse<WorkflowNodeHistoryData>>(`/api/v1/workflows/${id}/nodes`);
    return data;
  },

  async getEvents(id: string): Promise<WorkflowResponse<WorkflowEventListData>> {
    const { data } = await apiClient.get<WorkflowResponse<WorkflowEventListData>>(`/api/v1/workflows/${id}/events`);
    return data;
  },

  async getCheckpoints(id: string): Promise<WorkflowResponse<WorkflowCheckpointListData>> {
    const { data } = await apiClient.get<WorkflowResponse<WorkflowCheckpointListData>>(`/api/v1/workflows/${id}/checkpoints`);
    return data;
  },

  async getStatistics(id: string): Promise<WorkflowResponse<WorkflowStatisticsData>> {
    const { data } = await apiClient.get<WorkflowResponse<WorkflowStatisticsData>>(`/api/v1/workflows/${id}/statistics`);
    return data;
  }
};
