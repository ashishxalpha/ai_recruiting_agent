import { useQuery } from '@tanstack/react-query';
import { AgentService } from '@/services/agent.service';

export const agentKeys = {
  all: ['agents'] as const,
  overview: () => [...agentKeys.all, 'overview'] as const,
  runtime: (id: string) => [...agentKeys.all, id, 'runtime'] as const,
  sessions: (id: string) => [...agentKeys.all, id, 'sessions'] as const,
  thoughts: (id: string) => [...agentKeys.all, id, 'thoughts'] as const,
  actions: (id: string) => [...agentKeys.all, id, 'actions'] as const,
  tools: (id: string) => [...agentKeys.all, id, 'tools'] as const,
  memory: (id: string) => [...agentKeys.all, id, 'memory'] as const,
  reflection: (id: string) => [...agentKeys.all, id, 'reflection'] as const,
  replay: (id: string) => [...agentKeys.all, id, 'replay'] as const,
};

export function useAgentOverview() {
  return useQuery({
    queryKey: agentKeys.overview(),
    queryFn: () => AgentService.getOverview(),
  });
}

export function useAgentRuntime(agentId: string) {
  return useQuery({
    queryKey: agentKeys.runtime(agentId),
    queryFn: () => AgentService.getRuntime(agentId),
    enabled: !!agentId,
  });
}

export function useAgentSessions(agentId: string) {
  return useQuery({
    queryKey: agentKeys.sessions(agentId),
    queryFn: () => AgentService.getSessions(agentId),
    enabled: !!agentId,
  });
}

export function useAgentThoughts(agentId: string) {
  return useQuery({
    queryKey: agentKeys.thoughts(agentId),
    queryFn: () => AgentService.getThoughts(agentId),
    enabled: !!agentId,
  });
}

export function useAgentActions(agentId: string) {
  return useQuery({
    queryKey: agentKeys.actions(agentId),
    queryFn: () => AgentService.getActions(agentId),
    enabled: !!agentId,
  });
}

export function useAgentTools(agentId: string) {
  return useQuery({
    queryKey: agentKeys.tools(agentId),
    queryFn: () => AgentService.getTools(agentId),
    enabled: !!agentId,
  });
}

export function useAgentMemory(agentId: string) {
  return useQuery({
    queryKey: agentKeys.memory(agentId),
    queryFn: () => AgentService.getMemory(agentId),
    enabled: !!agentId,
  });
}

export function useAgentReflection(agentId: string) {
  return useQuery({
    queryKey: agentKeys.reflection(agentId),
    queryFn: () => AgentService.getReflection(agentId),
    enabled: !!agentId,
  });
}

export function useAgentReplay(agentId: string) {
  return useQuery({
    queryKey: agentKeys.replay(agentId),
    queryFn: () => AgentService.getReplay(agentId),
    enabled: !!agentId,
  });
}
