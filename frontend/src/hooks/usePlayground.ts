import { useQuery } from '@tanstack/react-query';
import { playgroundService } from '@/services/playground.service';

export function usePlaygroundDocument(documentId: string | null, stopPolling: boolean = false) {
  return useQuery({
    queryKey: ['playground', 'document', documentId],
    queryFn: () => documentId ? playgroundService.getDocument(documentId) : null,
    enabled: !!documentId,
    refetchInterval: (query: any) => {
      if (stopPolling) return false;
      const data = query.state?.data;
      if (!data) return 3000;
      // Stop polling once we have extracted text and candidate_id
      if (data.raw_text && data.candidate_id) return false;
      return 3000;
    }
  });
}

export function usePlaygroundStatus(documentId: string | null) {
  return useQuery({
    queryKey: ['playground', 'status', documentId],
    queryFn: () => documentId ? playgroundService.getDocumentStatus(documentId) : null,
    enabled: !!documentId,
    refetchInterval: (query: any) => {
      const data = query.state?.data;
      if (!data) return 3000;
      if (data.status === 'COMPLETED' || data.status === 'FAILED') return false;
      return 3000;
    }
  });
}

export function usePlaygroundExtraction(documentId: string | null, stopPolling: boolean = false) {
  return useQuery({
    queryKey: ['playground', 'extraction', documentId],
    queryFn: () => documentId ? playgroundService.getExtractionByDocument(documentId) : null,
    enabled: !!documentId,
    retry: false,
    refetchInterval: (query: any) => (query.state?.data || stopPolling) ? false : 3000
  });
}

export function usePlaygroundEmbeddings(candidateId: string | null, stopPolling: boolean = false) {
  return useQuery({
    queryKey: ['playground', 'embeddings', candidateId],
    queryFn: () => candidateId ? playgroundService.getEmbeddingsByCandidate(candidateId) : null,
    enabled: !!candidateId,
    retry: 3,
    refetchInterval: (query: any) => (stopPolling || (query.state?.data && query.state.data.length > 0)) ? false : 3000
  });
}

export function usePlaygroundEvaluation(candidateId: string | null, stopPolling: boolean = false) {
  return useQuery({
    queryKey: ['playground', 'evaluation', candidateId],
    queryFn: () => candidateId ? playgroundService.getEvaluationByCandidate(candidateId) : null,
    enabled: !!candidateId,
    retry: 3,
    refetchInterval: (query: any) => (stopPolling || (query.state?.data && query.state.data.length > 0)) ? false : 3000
  });
}
