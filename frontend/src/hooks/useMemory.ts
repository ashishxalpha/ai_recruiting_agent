import { useQuery } from '@tanstack/react-query';
import { MemoryService } from '@/services/memory.service';

export const memoryKeys = {
  all: ['memory'] as const,
  list: () => [...memoryKeys.all, 'list'] as const,
  detail: (id: string) => [...memoryKeys.all, 'detail', id] as const,
  search: (query: string, filters?: any) => [...memoryKeys.all, 'search', query, filters] as const,
  graph: () => [...memoryKeys.all, 'graph'] as const,
  timeline: (id: string) => [...memoryKeys.all, 'timeline', id] as const,
  relationships: (id: string) => [...memoryKeys.all, 'relationships', id] as const,
  statistics: () => [...memoryKeys.all, 'statistics'] as const,
  consolidations: () => [...memoryKeys.all, 'consolidations'] as const,
};

export function useMemoryList() {
  return useQuery({
    queryKey: memoryKeys.list(),
    queryFn: () => MemoryService.list(),
  });
}

export function useMemoryDetail(id: string) {
  return useQuery({
    queryKey: memoryKeys.detail(id),
    queryFn: () => MemoryService.getDetails(id),
    enabled: !!id,
  });
}

export function useMemorySearch(query: string, filters?: Record<string, any>) {
  return useQuery({
    queryKey: memoryKeys.search(query, filters),
    queryFn: () => MemoryService.search(query, filters),
    enabled: !!query,
  });
}

export function useMemoryGraph() {
  return useQuery({
    queryKey: memoryKeys.graph(),
    queryFn: () => MemoryService.getGraph(),
  });
}

export function useMemoryTimeline(id: string) {
  return useQuery({
    queryKey: memoryKeys.timeline(id),
    queryFn: () => MemoryService.getTimeline(id),
    enabled: !!id,
  });
}

export function useMemoryRelationships(id: string) {
  return useQuery({
    queryKey: memoryKeys.relationships(id),
    queryFn: () => MemoryService.getRelationships(id),
    enabled: !!id,
  });
}

export function useMemoryStatistics() {
  return useQuery({
    queryKey: memoryKeys.statistics(),
    queryFn: () => MemoryService.getStatistics(),
  });
}

export function useMemoryConsolidations() {
  return useQuery({
    queryKey: memoryKeys.consolidations(),
    queryFn: () => MemoryService.getConsolidations(),
  });
}
