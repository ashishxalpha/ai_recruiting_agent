import { Bot, Activity, History, Brain, Wrench, Hammer, Database, Lightbulb, PlaySquare } from "lucide-react";
import { 
  useAgentOverview, 
  useAgentRuntime, 
  useAgentSessions, 
  useAgentThoughts, 
  useAgentActions, 
  useAgentTools, 
  useAgentMemory, 
  useAgentReflection, 
  useAgentReplay 
} from "@/hooks/useAgent";
import { AgentWidgetWrapper } from "./AgentWidgetWrapper";

// Removed MOCK_AGENT_ID

export function AgentOverviewWidget() {
  const { data, isLoading, isError } = useAgentOverview();
  return (
    <AgentWidgetWrapper
      title="Agent Overview"
      description="List of registered autonomous agents."
      icon={<Bot className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(agents) => <pre>{JSON.stringify(agents, null, 2)}</pre>}
    </AgentWidgetWrapper>
  );
}

export function AgentRuntimeWidget() {
  const { data: overviewData } = useAgentOverview();
  const agentId = overviewData?.[0]?.id || "00000000-0000-0000-0000-000000000000";
  const { data, isLoading, isError } = useAgentRuntime(agentId);
  return (
    <AgentWidgetWrapper
      title="Runtime Metrics"
      description="Real-time execution status."
      icon={<Activity className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(runtime) => <pre>{JSON.stringify(runtime, null, 2)}</pre>}
    </AgentWidgetWrapper>
  );
}

export function AgentSessionsWidget() {
  const { data: overviewData } = useAgentOverview();
  const agentId = overviewData?.[0]?.id || "00000000-0000-0000-0000-000000000000";
  const { data, isLoading, isError } = useAgentSessions(agentId);
  return (
    <AgentWidgetWrapper
      title="Sessions"
      description="Active and historical agent sessions."
      icon={<History className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(sessions) => <pre>{JSON.stringify(sessions, null, 2)}</pre>}
    </AgentWidgetWrapper>
  );
}

export function AgentThoughtsWidget() {
  const { data: overviewData } = useAgentOverview();
  const agentId = overviewData?.[0]?.id || "00000000-0000-0000-0000-000000000000";
  const { data, isLoading, isError } = useAgentThoughts(agentId);
  return (
    <AgentWidgetWrapper
      title="Thoughts (Chain of Thought)"
      description="Agent reasoning and planning steps."
      icon={<Brain className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(thoughts) => <pre>{JSON.stringify(thoughts, null, 2)}</pre>}
    </AgentWidgetWrapper>
  );
}

export function AgentActionsWidget() {
  const { data: overviewData } = useAgentOverview();
  const agentId = overviewData?.[0]?.id || "00000000-0000-0000-0000-000000000000";
  const { data, isLoading, isError } = useAgentActions(agentId);
  return (
    <AgentWidgetWrapper
      title="Actions"
      description="Tool executions and their outcomes."
      icon={<Wrench className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(actions) => <pre>{JSON.stringify(actions, null, 2)}</pre>}
    </AgentWidgetWrapper>
  );
}

export function AgentToolsWidget() {
  const { data: overviewData } = useAgentOverview();
  const agentId = overviewData?.[0]?.id || "00000000-0000-0000-0000-000000000000";
  const { data, isLoading, isError } = useAgentTools(agentId);
  return (
    <AgentWidgetWrapper
      title="Tools"
      description="Tools registered for this agent."
      icon={<Hammer className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(tools) => <pre>{JSON.stringify(tools, null, 2)}</pre>}
    </AgentWidgetWrapper>
  );
}

export function AgentMemoryWidget() {
  const { data: overviewData } = useAgentOverview();
  const agentId = overviewData?.[0]?.id || "00000000-0000-0000-0000-000000000000";
  const { data, isLoading, isError } = useAgentMemory(agentId);
  return (
    <AgentWidgetWrapper
      title="Working Memory"
      description="Short-term context retained by the agent."
      icon={<Database className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(memory) => <pre>{JSON.stringify(memory, null, 2)}</pre>}
    </AgentWidgetWrapper>
  );
}

export function AgentReflectionWidget() {
  const { data: overviewData } = useAgentOverview();
  const agentId = overviewData?.[0]?.id || "00000000-0000-0000-0000-000000000000";
  const { data, isLoading, isError } = useAgentReflection(agentId);
  return (
    <AgentWidgetWrapper
      title="Reflection"
      description="Insights generated from self-correction."
      icon={<Lightbulb className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(reflection) => <pre>{JSON.stringify(reflection, null, 2)}</pre>}
    </AgentWidgetWrapper>
  );
}

export function AgentReplayWidget() {
  const { data: overviewData } = useAgentOverview();
  const agentId = overviewData?.[0]?.id || "00000000-0000-0000-0000-000000000000";
  const { data, isLoading, isError } = useAgentReplay(agentId);
  return (
    <AgentWidgetWrapper
      title="Session Replay"
      description="Time-travel debugging of agent execution."
      icon={<PlaySquare className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(replay) => <pre>{JSON.stringify(replay, null, 2)}</pre>}
    </AgentWidgetWrapper>
  );
}
