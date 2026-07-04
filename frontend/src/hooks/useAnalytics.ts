import { useQuery } from '@tanstack/react-query';
import { AnalyticsService } from '@/services/analytics.service';

export const analyticsKeys = {
  all: ['analytics'] as const,
  funnel: () => [...analyticsKeys.all, 'funnel'] as const,
  matching: () => [...analyticsKeys.all, 'matching'] as const,
  workflow: () => [...analyticsKeys.all, 'workflow'] as const,
  memory: () => [...analyticsKeys.all, 'memory'] as const,
  agent: () => [...analyticsKeys.all, 'agent'] as const,
  tools: () => [...analyticsKeys.all, 'tools'] as const,
  organization: () => [...analyticsKeys.all, 'organization'] as const,
  health: () => [...analyticsKeys.all, 'health'] as const,
};

export function useAnalyticsFunnel() {
  return useQuery({
    queryKey: analyticsKeys.funnel(),
    queryFn: () => AnalyticsService.getFunnel(),
  });
}

export function useAnalyticsMatching() {
  return useQuery({
    queryKey: analyticsKeys.matching(),
    queryFn: () => AnalyticsService.getMatching(),
  });
}

export function useAnalyticsWorkflow() {
  return useQuery({
    queryKey: analyticsKeys.workflow(),
    queryFn: () => AnalyticsService.getWorkflow(),
  });
}

export function useAnalyticsMemory() {
  return useQuery({
    queryKey: analyticsKeys.memory(),
    queryFn: () => AnalyticsService.getMemory(),
  });
}

export function useAnalyticsAgent() {
  return useQuery({
    queryKey: analyticsKeys.agent(),
    queryFn: () => AnalyticsService.getAgent(),
  });
}

export function useAnalyticsTools() {
  return useQuery({
    queryKey: analyticsKeys.tools(),
    queryFn: () => AnalyticsService.getTools(),
  });
}

export function useAnalyticsOrganization() {
  return useQuery({
    queryKey: analyticsKeys.organization(),
    queryFn: () => AnalyticsService.getOrganization(),
  });
}

export function useAnalyticsHealth() {
  return useQuery({
    queryKey: analyticsKeys.health(),
    queryFn: () => AnalyticsService.getHealth(),
  });
}
