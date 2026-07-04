import { useQuery } from '@tanstack/react-query';
import { WorkflowService } from '@/services/workflow.service';

export const workflowKeys = {
  all: ['workflow'] as const,
  detail: (id: string) => [...workflowKeys.all, 'detail', id] as const,
  timeline: (id: string) => [...workflowKeys.all, 'timeline', id] as const,
  graph: (id: string) => [...workflowKeys.all, 'graph', id] as const,
  nodes: (id: string) => [...workflowKeys.all, 'nodes', id] as const,
  events: (id: string) => [...workflowKeys.all, 'events', id] as const,
  checkpoints: (id: string) => [...workflowKeys.all, 'checkpoints', id] as const,
  statistics: (id: string) => [...workflowKeys.all, 'statistics', id] as const,
};

export function useWorkflowSummary(id: string) {
  return useQuery({
    queryKey: workflowKeys.detail(id),
    queryFn: () => WorkflowService.getSummary(id),
    enabled: !!id,
  });
}

export function useWorkflowTimeline(id: string) {
  return useQuery({
    queryKey: workflowKeys.timeline(id),
    queryFn: () => WorkflowService.getTimeline(id),
    enabled: !!id,
  });
}

export function useWorkflowGraph(id: string) {
  return useQuery({
    queryKey: workflowKeys.graph(id),
    queryFn: () => WorkflowService.getGraph(id),
    enabled: !!id,
  });
}

export function useWorkflowNodes(id: string) {
  return useQuery({
    queryKey: workflowKeys.nodes(id),
    queryFn: () => WorkflowService.getNodes(id),
    enabled: !!id,
  });
}

export function useWorkflowEvents(id: string) {
  return useQuery({
    queryKey: workflowKeys.events(id),
    queryFn: () => WorkflowService.getEvents(id),
    enabled: !!id,
  });
}

export function useWorkflowCheckpoints(id: string) {
  return useQuery({
    queryKey: workflowKeys.checkpoints(id),
    queryFn: () => WorkflowService.getCheckpoints(id),
    enabled: !!id,
  });
}

export function useWorkflowStatistics(id: string) {
  return useQuery({
    queryKey: workflowKeys.statistics(id),
    queryFn: () => WorkflowService.getStatistics(id),
    enabled: !!id,
  });
}
