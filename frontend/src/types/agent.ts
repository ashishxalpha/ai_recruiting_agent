import { StandardResponse } from "./dashboard";

export interface AgentRuntime {
  id: string;
  status: string;
  current_task: string | null;
  uptime: number;
}

export interface AgentSession {
  session_id: string;
  started_at: string;
  duration: number;
}

export interface AgentThought {
  thought_id: string;
  timestamp: string;
  content: string;
  confidence: number;
}

export interface AgentAction {
  action_id: string;
  timestamp: string;
  tool_name: string;
  input: Record<string, any>;
  result: string;
}

export interface AgentTool {
  tool_name: string;
  description: string;
  usage_count: number;
}

export interface AgentMemory {
  memory_id: string;
  content: string;
  relevance: number;
}

export interface AgentReflection {
  reflection_id: string;
  timestamp: string;
  insight: string;
}

export interface AgentReplay {
  events: Record<string, any>[];
}
