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
    const response = await apiClient.get<any, StandardResponse<any[]>>(`/api/v1/agents`);
    return response;
  },

  async getRuntime(agentId: string): Promise<StandardResponse<AgentRuntime>> {
    const response = await apiClient.get<any, StandardResponse<AgentRuntime>>(`/api/v1/agents/${agentId}/runtime`);
    return response;
  },

  async getSessions(agentId: string): Promise<StandardResponse<AgentSession[]>> {
    const response = await apiClient.get<any, StandardResponse<AgentSession[]>>(`/api/v1/agents/${agentId}/sessions`);
    return response;
  },

  async getThoughts(agentId: string): Promise<StandardResponse<AgentThought[]>> {
    const response = await apiClient.get<any, StandardResponse<AgentThought[]>>(`/api/v1/agents/${agentId}/thoughts`);
    return response;
  },

  async getActions(agentId: string): Promise<StandardResponse<AgentAction[]>> {
    const response = await apiClient.get<any, StandardResponse<AgentAction[]>>(`/api/v1/agents/${agentId}/actions`);
    return response;
  },

  async getTools(agentId: string): Promise<StandardResponse<AgentTool[]>> {
    const response = await apiClient.get<any, StandardResponse<AgentTool[]>>(`/api/v1/agents/${agentId}/tools`);
    return response;
  },

  async getMemory(agentId: string): Promise<StandardResponse<AgentMemory[]>> {
    const response = await apiClient.get<any, StandardResponse<AgentMemory[]>>(`/api/v1/agents/${agentId}/memory`);
    return response;
  },

  async getReflection(agentId: string): Promise<StandardResponse<AgentReflection[]>> {
    const response = await apiClient.get<any, StandardResponse<AgentReflection[]>>(`/api/v1/agents/${agentId}/reflection`);
    return response;
  },

  async getReplay(agentId: string): Promise<StandardResponse<AgentReplay>> {
    const response = await apiClient.get<any, StandardResponse<AgentReplay>>(`/api/v1/agents/${agentId}/replay`);
    return response;
  }
};
