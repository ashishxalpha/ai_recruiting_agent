import { useQuery } from '@tanstack/react-query';
import { OrganizationService } from '@/services/organization.service';

export const organizationKeys = {
  all: ['organization'] as const,
  overview: () => [...organizationKeys.all, 'overview'] as const,
  goals: () => [...organizationKeys.all, 'goals'] as const,
  roles: () => [...organizationKeys.all, 'roles'] as const,
  skills: () => [...organizationKeys.all, 'skills'] as const,
  executions: () => [...organizationKeys.all, 'executions'] as const,
  policies: () => [...organizationKeys.all, 'policies'] as const,
  learning: () => [...organizationKeys.all, 'learning'] as const,
  metrics: () => [...organizationKeys.all, 'metrics'] as const,
  activity: () => [...organizationKeys.all, 'activity'] as const,
};

export function useOrganizationOverview() {
  return useQuery({
    queryKey: organizationKeys.overview(),
    queryFn: () => OrganizationService.getOverview(),
  });
}

export function useOrganizationGoals() {
  return useQuery({
    queryKey: organizationKeys.goals(),
    queryFn: () => OrganizationService.getGoals(),
  });
}

export function useOrganizationRoles() {
  return useQuery({
    queryKey: organizationKeys.roles(),
    queryFn: () => OrganizationService.getRoles(),
  });
}

export function useOrganizationSkills() {
  return useQuery({
    queryKey: organizationKeys.skills(),
    queryFn: () => OrganizationService.getSkills(),
  });
}

export function useOrganizationExecutions() {
  return useQuery({
    queryKey: organizationKeys.executions(),
    queryFn: () => OrganizationService.getExecutions(),
  });
}

export function useOrganizationPolicies() {
  return useQuery({
    queryKey: organizationKeys.policies(),
    queryFn: () => OrganizationService.getPolicies(),
  });
}

export function useOrganizationLearning() {
  return useQuery({
    queryKey: organizationKeys.learning(),
    queryFn: () => OrganizationService.getLearning(),
  });
}

export function useOrganizationMetrics() {
  return useQuery({
    queryKey: organizationKeys.metrics(),
    queryFn: () => OrganizationService.getMetrics(),
  });
}

export function useOrganizationActivity() {
  return useQuery({
    queryKey: organizationKeys.activity(),
    queryFn: () => OrganizationService.getActivity(),
  });
}
