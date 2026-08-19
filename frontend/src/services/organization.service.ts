import { apiClient } from "@/lib/api-client";
import { StandardResponse } from "@/types/dashboard";
import {
  OrganizationGoal,
  OrganizationRole,
  OrganizationSkill,
  OrganizationExecution,
  OrganizationPolicy,
  OrganizationLearning,
  OrganizationMetric,
  OrganizationActivity
} from "@/types/organization";

export const OrganizationService = {
  async getOverview(): Promise<StandardResponse<any>> {
    const response = await apiClient.get<any, StandardResponse<any>>(`/api/v1/organization`);
    return response;
  },
  
  async getGoals(): Promise<StandardResponse<OrganizationGoal[]>> {
    const response = await apiClient.get<any, StandardResponse<OrganizationGoal[]>>(`/api/v1/organization/goals`);
    return response;
  },

  async getRoles(): Promise<StandardResponse<OrganizationRole[]>> {
    const response = await apiClient.get<any, StandardResponse<OrganizationRole[]>>(`/api/v1/organization/roles`);
    return response;
  },

  async getSkills(): Promise<StandardResponse<OrganizationSkill[]>> {
    const response = await apiClient.get<any, StandardResponse<OrganizationSkill[]>>(`/api/v1/organization/skills`);
    return response;
  },

  async getExecutions(): Promise<StandardResponse<OrganizationExecution[]>> {
    const response = await apiClient.get<any, StandardResponse<OrganizationExecution[]>>(`/api/v1/organization/executions`);
    return response;
  },

  async getPolicies(): Promise<StandardResponse<OrganizationPolicy[]>> {
    const response = await apiClient.get<any, StandardResponse<OrganizationPolicy[]>>(`/api/v1/organization/policies`);
    return response;
  },

  async getLearning(): Promise<StandardResponse<OrganizationLearning[]>> {
    const response = await apiClient.get<any, StandardResponse<OrganizationLearning[]>>(`/api/v1/organization/learning`);
    return response;
  },

  async getMetrics(): Promise<StandardResponse<OrganizationMetric[]>> {
    const response = await apiClient.get<any, StandardResponse<OrganizationMetric[]>>(`/api/v1/organization/metrics`);
    return response;
  },

  async getActivity(): Promise<StandardResponse<OrganizationActivity[]>> {
    const response = await apiClient.get<any, StandardResponse<OrganizationActivity[]>>(`/api/v1/organization/activity`);
    return response;
  }
};
