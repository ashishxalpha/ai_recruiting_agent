export type MemoryStatus = "available" | "not_available" | "loading" | "error" | "no_data";

export interface MemoryResponse<T> {
  status: MemoryStatus;
  reason?: string;
  data?: T | null;
}

export interface MemorySummary {
  id: string;
  namespace: string;
  memory_type: string;
  content_snippet: string;
  importance: number;
  confidence: number;
  created_at: string;
  last_accessed_at: string;
}

export interface MemoryList {
  memories: MemorySummary[];
  total_count: number;
}

export interface MemoryDetails {
  id: string;
  namespace: string;
  memory_type: string;
  content: string;
  metadata: Record<string, any>;
  importance: number;
  confidence: number;
  created_at: string;
  updated_at: string;
  last_accessed_at: string;
  source_id?: string;
}

export interface MemoryRetrievalCandidate {
  memory_id: string;
  content_snippet: string;
  similarity_score: number;
  reranking_score: number;
  importance: number;
  recency: number;
  decay: number;
  confidence: number;
  final_ranking: number;
  inclusion_reason?: string;
  exclusion_reason?: string;
}

export interface MemoryRetrieval {
  query: string;
  namespace?: string;
  retrieval_policy: string;
  embedding_model: string;
  execution_time_ms: number;
  candidates: MemoryRetrievalCandidate[];
}

export interface MemoryGraphNode {
  id: string;
  type: string;
  data: Record<string, any>;
  position: { x: number; y: number };
}

export interface MemoryGraphEdge {
  id: string;
  source: string;
  target: string;
  label: string;
  type?: string;
  data: Record<string, any>;
}

export interface MemoryGraphData {
  nodes: MemoryGraphNode[];
  edges: MemoryGraphEdge[];
}

export interface MemoryTimelineEntry {
  event_id: string;
  memory_id: string;
  timestamp: string;
  event_type: string;
  actor: string;
  workflow_id?: string;
  agent_id?: string;
  source: string;
  metadata: Record<string, any>;
}

export interface MemoryTimelineData {
  entries: MemoryTimelineEntry[];
}

export interface MemoryRelationship {
  source_id: string;
  target_id: string;
  relationship_type: string;
  strength: number;
  metadata: Record<string, any>;
}

export interface MemoryRelationshipListData {
  relationships: MemoryRelationship[];
}

export interface MemoryConsolidationEvent {
  consolidation_id: string;
  timestamp: string;
  input_memory_ids: string[];
  output_memory_id?: string;
  summary_generated?: string;
  deduplication_occurred: boolean;
  importance_change: number;
  decay_update: number;
  latency_ms: number;
}

export interface MemoryConsolidationData {
  consolidations: MemoryConsolidationEvent[];
}

export interface MemoryStatistics {
  total_memories: number;
  namespaces: Record<string, number>;
  memory_types: Record<string, number>;
  average_importance: number;
  average_confidence: number;
  decay_distribution: Record<string, number>;
  total_retrievals: number;
  average_retrieval_latency_ms: number;
  consolidation_count: number;
  relationship_count: number;
}
