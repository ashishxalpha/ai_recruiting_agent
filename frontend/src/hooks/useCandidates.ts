import { useQuery } from '@tanstack/react-query';
import { CandidateService, CandidateListParams } from '@/services/candidate.service';

export const candidateKeys = {
  all: ['candidates'] as const,
  lists: () => [...candidateKeys.all, 'list'] as const,
  list: (params: CandidateListParams) => [...candidateKeys.lists(), params] as const,
  details: () => [...candidateKeys.all, 'detail'] as const,
  detail: (id: string) => [...candidateKeys.details(), id] as const,
  workflow: (id: string) => [...candidateKeys.detail(id), 'workflow'] as const,
  evaluation: (id: string) => [...candidateKeys.detail(id), 'evaluation'] as const,
  embeddings: (id: string) => [...candidateKeys.detail(id), 'embeddings'] as const,
  memory: (id: string) => [...candidateKeys.detail(id), 'memory'] as const,
  matches: (id: string) => [...candidateKeys.detail(id), 'matches'] as const,
  feedback: (id: string) => [...candidateKeys.detail(id), 'feedback'] as const,
  documents: (id: string) => [...candidateKeys.detail(id), 'documents'] as const,
};

export function useCandidateList(params: CandidateListParams) {
  return useQuery({
    queryKey: candidateKeys.list(params),
    queryFn: () => CandidateService.listCandidates(params),
    staleTime: 5 * 60 * 1000, // 5 mins
  });
}

export function useCandidateDetails(id: string) {
  return useQuery({
    queryKey: candidateKeys.detail(id),
    queryFn: () => CandidateService.getDetails(id),
    staleTime: 5 * 60 * 1000,
    enabled: !!id,
  });
}

export function useCandidateWorkflow(id: string) {
  return useQuery({
    queryKey: candidateKeys.workflow(id),
    queryFn: () => CandidateService.getWorkflow(id),
    enabled: !!id,
  });
}

export function useCandidateEvaluation(id: string) {
  return useQuery({
    queryKey: candidateKeys.evaluation(id),
    queryFn: () => CandidateService.getEvaluation(id),
    enabled: !!id,
  });
}

export function useCandidateEmbeddings(id: string) {
  return useQuery({
    queryKey: candidateKeys.embeddings(id),
    queryFn: () => CandidateService.getEmbeddings(id),
    enabled: !!id,
  });
}

export function useCandidateMemory(id: string) {
  return useQuery({
    queryKey: candidateKeys.memory(id),
    queryFn: () => CandidateService.getMemory(id),
    enabled: !!id,
  });
}

export function useCandidateMatches(id: string) {
  return useQuery({
    queryKey: candidateKeys.matches(id),
    queryFn: () => CandidateService.getMatches(id),
    enabled: !!id,
  });
}

export function useCandidateFeedback(id: string) {
  return useQuery({
    queryKey: candidateKeys.feedback(id),
    queryFn: () => CandidateService.getFeedback(id),
    enabled: !!id,
  });
}

export function useCandidateDocuments(id: string) {
  return useQuery({
    queryKey: candidateKeys.documents(id),
    queryFn: () => CandidateService.getDocuments(id),
    enabled: !!id,
  });
}
