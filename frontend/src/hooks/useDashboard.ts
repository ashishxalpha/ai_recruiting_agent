import { useQuery } from '@tanstack/react-query';
import { DashboardService } from '@/services/dashboard.service';

export const dashboardKeys = {
  all: ['dashboard'] as const,
  summary: () => [...dashboardKeys.all, 'summary'] as const,
  health: () => [...dashboardKeys.all, 'health'] as const,
  activity: (limit: number) => [...dashboardKeys.all, 'activity', limit] as const,
};

export function useDashboardSummary() {
  return useQuery({
    queryKey: dashboardKeys.summary(),
    queryFn: () => DashboardService.getSummary(),
  });
}

export function useDashboardHealth() {
  return useQuery({
    queryKey: dashboardKeys.health(),
    queryFn: () => DashboardService.getHealth(),
  });
}

export function useRecentActivity(limit: number = 20) {
  return useQuery({
    queryKey: dashboardKeys.activity(limit),
    queryFn: () => DashboardService.getActivity(limit),
  });
}
