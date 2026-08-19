import { apiClient } from "@/lib/api-client";

export const ToolsService = {
  async getCapabilities(): Promise<any[]> {
    const response = await apiClient.get<any, any[]>(`/api/v1/tools/capabilities`);
    return response;
  }
};
