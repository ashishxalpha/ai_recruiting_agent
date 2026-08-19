import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';

export interface IngestionItem {
  id: string;
  filename: string;
  status: string;
  created_at: string;
  candidate_id?: string;
  error_message?: string;
}

export const ingestionKeys = {
  all: ['ingestions'] as const,
  recent: () => [...ingestionKeys.all, 'recent'] as const,
};

export function useRecentIngestions() {
  return useQuery({
    queryKey: ingestionKeys.recent(),
    queryFn: async () => {
      const response = await apiClient.get<any, IngestionItem[]>('/api/v1/resumes/ingestions');
      return response;
    },
    refetchInterval: (query) => {
      // Poll every 3 seconds if any item is still processing
      const data = query.state.data;
      if (!data) return false;
      const isProcessing = data.some(item => item.status === 'QUEUED' || item.status === 'RUNNING');
      return isProcessing ? 3000 : false;
    }
  });
}
