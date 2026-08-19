import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';

export interface PendingMatch {
  id: string;
  candidate: string;
  job: string;
  score: number;
  status: string;
  created_at: string;
}

export interface FeedbackCreateRequest {
  decision: "APPROVED" | "REJECTED";
  confidence?: number;
  reason?: string;
  notes?: string;
}

export const feedbackKeys = {
  all: ['feedback'] as const,
  pending: () => [...feedbackKeys.all, 'pending'] as const,
};

export function usePendingFeedback() {
  return useQuery({
    queryKey: feedbackKeys.pending(),
    queryFn: async () => {
      return apiClient.get<any, PendingMatch[]>('/api/v1/feedback/pending');
    },
  });
}

export function useSubmitFeedback() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ matchId, data }: { matchId: string, data: FeedbackCreateRequest }) => {
      return apiClient.post(`/api/v1/feedback/matches/${matchId}/feedback`, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: feedbackKeys.pending() });
      // We could also invalidate specific match/job queries if needed
    },
  });
}
