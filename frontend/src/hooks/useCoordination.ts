import { useQuery } from '@tanstack/react-query';
import { CoordinationService } from '@/services/coordination.service';

export const coordinationKeys = {
  all: ['coordination'] as const,
  overview: () => [...coordinationKeys.all, 'overview'] as const,
  sessions: () => [...coordinationKeys.all, 'sessions'] as const,
  consensus: () => [...coordinationKeys.all, 'consensus'] as const,
  handoffs: () => [...coordinationKeys.all, 'handoffs'] as const,
  conflicts: () => [...coordinationKeys.all, 'conflicts'] as const,
};

export function useCoordinationOverview() {
  return useQuery({
    queryKey: coordinationKeys.overview(),
    queryFn: () => CoordinationService.getOverview(),
  });
}

export function useCoordinationSessions() {
  return useQuery({
    queryKey: coordinationKeys.sessions(),
    queryFn: () => CoordinationService.getSessions(),
  });
}

export function useCoordinationConsensus() {
  return useQuery({
    queryKey: coordinationKeys.consensus(),
    queryFn: () => CoordinationService.getConsensus(),
  });
}

export function useCoordinationHandoffs() {
  return useQuery({
    queryKey: coordinationKeys.handoffs(),
    queryFn: () => CoordinationService.getHandoffs(),
  });
}

export function useCoordinationConflicts() {
  return useQuery({
    queryKey: coordinationKeys.conflicts(),
    queryFn: () => CoordinationService.getConflicts(),
  });
}
