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
    const { data } = await apiClient.get<StandardResponse<any>>(`/api/v1/organization`);
    return data;
  },
  
  async getGoals(): Promise<StandardResponse<OrganizationGoal[]>> {
    const { data } = await apiClient.get<StandardResponse<OrganizationGoal[]>>(`/api/v1/organization/goals`);
    return data;
  },

  async getRoles(): Promise<StandardResponse<OrganizationRole[]>> {
    const { data } = await apiClient.get<StandardResponse<OrganizationRole[]>>(`/api/v1/organization/roles`);
    return data;
  },

  async getSkills(): Promise<StandardResponse<OrganizationSkill[]>> {
    const { data } = await apiClient.get<StandardResponse<OrganizationSkill[]>>(`/api/v1/organization/skills`);
    return data;
  },

  async getExecutions(): Promise<StandardResponse<OrganizationExecution[]>> {
    const { data } = await apiClient.get<StandardResponse<OrganizationExecution[]>>(`/api/v1/organization/executions`);
    return data;
  },

  async getPolicies(): Promise<StandardResponse<OrganizationPolicy[]>> {
    const { data } = await apiClient.get<StandardResponse<OrganizationPolicy[]>>(`/api/v1/organization/policies`);
    return data;
  },

  async getLearning(): Promise<StandardResponse<OrganizationLearning[]>> {
    const { data } = await apiClient.get<StandardResponse<OrganizationLearning[]>>(`/api/v1/organization/learning`);
    return data;
  },

  async getMetrics(): Promise<StandardResponse<OrganizationMetric[]>> {
    const { data } = await apiClient.get<StandardResponse<OrganizationMetric[]>>(`/api/v1/organization/metrics`);
    return data;
  },

  async getActivity(): Promise<StandardResponse<OrganizationActivity[]>> {
    const { data } = await apiClient.get<StandardResponse<OrganizationActivity[]>>(`/api/v1/organization/activity`);
    return data;
  }
};
