import { useQuery } from '@tanstack/react-query';
import { JobService, JobListParams } from '@/services/job.service';

export const jobKeys = {
  all: ['jobs'] as const,
  lists: () => [...jobKeys.all, 'list'] as const,
  list: (params: JobListParams) => [...jobKeys.lists(), params] as const,
  details: () => [...jobKeys.all, 'detail'] as const,
  detail: (id: string) => [...jobKeys.details(), id] as const,
  candidates: (id: string) => [...jobKeys.detail(id), 'candidates'] as const,
  matches: (id: string) => [...jobKeys.detail(id), 'matches'] as const,
  workflow: (id: string) => [...jobKeys.detail(id), 'workflow'] as const,
  analytics: (id: string) => [...jobKeys.detail(id), 'analytics'] as const,
  feedback: (id: string) => [...jobKeys.detail(id), 'feedback'] as const,
  documents: (id: string) => [...jobKeys.detail(id), 'documents'] as const,
  history: (id: string) => [...jobKeys.detail(id), 'history'] as const,
};

export function useJobList(params: JobListParams) {
  return useQuery({
    queryKey: jobKeys.list(params),
    queryFn: () => JobService.listJobs(params),
    staleTime: 5 * 60 * 1000,
  });
}

export function useJobDetails(id: string) {
  return useQuery({
    queryKey: jobKeys.detail(id),
    queryFn: () => JobService.getDetails(id),
    staleTime: 5 * 60 * 1000,
    enabled: !!id,
  });
}

export function useJobCandidates(id: string) {
  return useQuery({
    queryKey: jobKeys.candidates(id),
    queryFn: () => JobService.getCandidates(id),
    enabled: !!id,
  });
}

export function useJobMatches(id: string) {
  return useQuery({
    queryKey: jobKeys.matches(id),
    queryFn: () => JobService.getMatches(id),
    enabled: !!id,
  });
}

export function useJobWorkflow(id: string) {
  return useQuery({
    queryKey: jobKeys.workflow(id),
    queryFn: () => JobService.getWorkflow(id),
    enabled: !!id,
  });
}

export function useJobAnalytics(id: string) {
  return useQuery({
    queryKey: jobKeys.analytics(id),
    queryFn: () => JobService.getAnalytics(id),
    enabled: !!id,
  });
}

export function useJobFeedback(id: string) {
  return useQuery({
    queryKey: jobKeys.feedback(id),
    queryFn: () => JobService.getFeedback(id),
    enabled: !!id,
  });
}

export function useJobDocuments(id: string) {
  return useQuery({
    queryKey: jobKeys.documents(id),
    queryFn: () => JobService.getDocuments(id),
    enabled: !!id,
  });
}

export function useJobHistory(id: string) {
  return useQuery({
    queryKey: jobKeys.history(id),
    queryFn: () => JobService.getHistory(id),
    enabled: !!id,
  });
}
