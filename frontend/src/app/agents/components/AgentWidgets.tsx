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

// Currently, we don't have a way to select a specific agent in the UI to pass its ID.
// For the sake of this mock removal, we'll hardcode an agent ID or handle the overview.
const MOCK_AGENT_ID = "00000000-0000-0000-0000-000000000000";

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
  const { data, isLoading, isError } = useAgentRuntime(MOCK_AGENT_ID);
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
  const { data, isLoading, isError } = useAgentSessions(MOCK_AGENT_ID);
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
  const { data, isLoading, isError } = useAgentThoughts(MOCK_AGENT_ID);
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
  const { data, isLoading, isError } = useAgentActions(MOCK_AGENT_ID);
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
  const { data, isLoading, isError } = useAgentTools(MOCK_AGENT_ID);
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
  const { data, isLoading, isError } = useAgentMemory(MOCK_AGENT_ID);
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
  const { data, isLoading, isError } = useAgentReflection(MOCK_AGENT_ID);
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
  const { data, isLoading, isError } = useAgentReplay(MOCK_AGENT_ID);
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
