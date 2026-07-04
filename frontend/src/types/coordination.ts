import { StandardResponse } from "./dashboard";

export interface CoordinationSession {
  session_id: string;
  status: string;
  active_agents: number;
  started_at: string;
}

export interface CoordinationConsensus {
  decision_id: string;
  topic: string;
  resolution: string;
  agents_involved: string[];
}

export interface CoordinationHandoff {
  handoff_id: string;
  from_agent: string;
  to_agent: string;
  reason: string;
  timestamp: string;
}

export interface CoordinationConflict {
  conflict_id: string;
  issue: string;
  status: string;
  resolved_by: string | null;
}
