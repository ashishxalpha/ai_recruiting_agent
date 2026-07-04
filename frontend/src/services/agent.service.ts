import { apiClient } from "@/lib/api-client";
import { StandardResponse } from "@/types/dashboard";
import {
  AgentRuntime,
  AgentSession,
  AgentThought,
  AgentAction,
  AgentTool,
  AgentMemory,
  AgentReflection,
  AgentReplay
} from "@/types/agent";

export const AgentService = {
  async getOverview(): Promise<StandardResponse<any[]>> {
    const { data } = await apiClient.get<StandardResponse<any[]>>(`/api/v1/agents`);
    return data;
  },

  async getRuntime(agentId: string): Promise<StandardResponse<AgentRuntime>> {
    const { data } = await apiClient.get<StandardResponse<AgentRuntime>>(`/api/v1/agents/${agentId}/runtime`);
    return data;
  },

  async getSessions(agentId: string): Promise<StandardResponse<AgentSession[]>> {
    const { data } = await apiClient.get<StandardResponse<AgentSession[]>>(`/api/v1/agents/${agentId}/sessions`);
    return data;
  },

  async getThoughts(agentId: string): Promise<StandardResponse<AgentThought[]>> {
    const { data } = await apiClient.get<StandardResponse<AgentThought[]>>(`/api/v1/agents/${agentId}/thoughts`);
    return data;
  },

  async getActions(agentId: string): Promise<StandardResponse<AgentAction[]>> {
    const { data } = await apiClient.get<StandardResponse<AgentAction[]>>(`/api/v1/agents/${agentId}/actions`);
    return data;
  },

  async getTools(agentId: string): Promise<StandardResponse<AgentTool[]>> {
    const { data } = await apiClient.get<StandardResponse<AgentTool[]>>(`/api/v1/agents/${agentId}/tools`);
    return data;
  },

  async getMemory(agentId: string): Promise<StandardResponse<AgentMemory[]>> {
    const { data } = await apiClient.get<StandardResponse<AgentMemory[]>>(`/api/v1/agents/${agentId}/memory`);
    return data;
  },

  async getReflection(agentId: string): Promise<StandardResponse<AgentReflection[]>> {
    const { data } = await apiClient.get<StandardResponse<AgentReflection[]>>(`/api/v1/agents/${agentId}/reflection`);
    return data;
  },

  async getReplay(agentId: string): Promise<StandardResponse<AgentReplay>> {
    const { data } = await apiClient.get<StandardResponse<AgentReplay>>(`/api/v1/agents/${agentId}/replay`);
    return data;
  }
};
