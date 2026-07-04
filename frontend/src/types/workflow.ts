export type WorkflowStatus = "available" | "not_available" | "loading" | "error" | "no_execution_history";

export interface WorkflowResponse<T> {
  status: WorkflowStatus;
  reason?: string;
  data?: T | null;
}

export interface WorkflowSummaryData {
  id: string;
  job_id?: string;
  candidate_id?: string;
  status: string;
  started_at?: string;
  completed_at?: string;
  current_node?: string;
  workflow_version: string;
}

export interface WorkflowGraphNode {
  id: string;
  type: string;
  data: Record<string, any>;
  position: { x: number; y: number };
}

export interface WorkflowGraphEdge {
  id: string;
  source: string;
  target: string;
  label?: string;
  type?: string;
}

export interface WorkflowGraphData {
  nodes: WorkflowGraphNode[];
  edges: WorkflowGraphEdge[];
  current_node_id?: string;
}

export interface WorkflowTimelineEntry {
  event_id: string;
  workflow_id: string;
  timestamp: string;
  state: string;
  node_id?: string;
  duration_ms?: number;
  metadata: Record<string, any>;
}

export interface WorkflowTimelineData {
  entries: WorkflowTimelineEntry[];
}

export interface WorkflowNodeExecution {
  node_id: string;
  status: string;
  start_time?: string;
  end_time?: string;
  duration_ms?: number;
  retries: number;
  inputs: Record<string, any>;
  outputs: Record<string, any>;
  errors: string[];
  warnings: string[];
  tool_invocations: number;
  memory_retrievals: number;
}

export interface WorkflowNodeHistoryData {
  executions: WorkflowNodeExecution[];
}

export interface WorkflowEvent {
  event_id: string;
  timestamp: string;
  category: string;
  severity: string;
  message: string;
  node_id?: string;
  metadata: Record<string, any>;
}

export interface WorkflowEventListData {
  events: WorkflowEvent[];
}

export interface WorkflowCheckpoint {
  checkpoint_id: string;
  created_at: string;
  resumed_at?: string;
  rollback_available: boolean;
  workflow_version: string;
  graph_version: string;
  prompt_version: string;
  metadata: Record<string, any>;
  state_snapshot: Record<string, any>;
}

export interface WorkflowCheckpointListData {
  checkpoints: WorkflowCheckpoint[];
}

export interface WorkflowStatisticsData {
  total_duration_ms: number;
  average_node_time_ms: number;
  retries: number;
  failures: number;
  human_approvals: number;
  checkpoint_count: number;
  tool_calls: number;
  memory_retrievals: number;
}
