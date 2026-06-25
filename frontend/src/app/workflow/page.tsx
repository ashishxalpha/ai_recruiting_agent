"use client";

import { useCallback, useEffect, useState } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  Edge
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { useSSE } from "@/lib/hooks/use-sse";

const initialNodes = [
  { id: 'UploadValidationNode', position: { x: 250, y: 50 }, data: { label: 'Resume Upload' }, style: { border: '1px solid #3b82f6', borderRadius: '8px', padding: '10px' } },
  { id: 'DocumentParsingNode', position: { x: 250, y: 150 }, data: { label: 'Text Extraction' }, style: { border: '1px solid #3b82f6', borderRadius: '8px', padding: '10px' } },
  { id: 'AIExtractionNode', position: { x: 250, y: 250 }, data: { label: 'AI Normalization' }, style: { border: '1px solid #3b82f6', borderRadius: '8px', padding: '10px' } },
  { id: 'EmbeddingGenerationNode', position: { x: 100, y: 350 }, data: { label: 'Vector Embeddings' }, style: { border: '1px solid #3b82f6', borderRadius: '8px', padding: '10px' } },
  { id: 'ProfileEvaluationNode', position: { x: 400, y: 350 }, data: { label: 'Profile Evaluation' }, style: { border: '1px solid #3b82f6', borderRadius: '8px', padding: '10px' } },
  { id: 'CandidateMatchingNode', position: { x: 250, y: 450 }, data: { label: 'Candidate Match' }, style: { border: '1px solid #3b82f6', borderRadius: '8px', padding: '10px' } },
  { id: 'HumanApprovalNode', position: { x: 250, y: 550 }, data: { label: 'Recruiter Feedback' }, style: { border: '1px solid #3b82f6', borderRadius: '8px', padding: '10px' } },
];

const initialEdges = [
  { id: 'e1-2', source: 'UploadValidationNode', target: 'DocumentParsingNode', animated: true },
  { id: 'e2-3', source: 'DocumentParsingNode', target: 'AIExtractionNode', animated: true },
  { id: 'e3-4', source: 'AIExtractionNode', target: 'EmbeddingGenerationNode', animated: true },
  { id: 'e3-5', source: 'AIExtractionNode', target: 'ProfileEvaluationNode', animated: true },
  { id: 'e4-6', source: 'EmbeddingGenerationNode', target: 'CandidateMatchingNode', animated: true },
  { id: 'e5-6', source: 'ProfileEvaluationNode', target: 'CandidateMatchingNode', animated: true },
  { id: 'e6-7', source: 'CandidateMatchingNode', target: 'HumanApprovalNode', animated: false },
];

export default function WorkflowPage() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const { lastEvent } = useSSE("http://localhost:8000/api/v1/stream");

  useEffect(() => {
    if (lastEvent && lastEvent.type.includes('WorkflowNode')) {
      const nodeName = lastEvent.data.node_name;
      setNodes((nds) => 
        nds.map((node) => {
          if (node.id === nodeName) {
            let color = '#3b82f6'; // default blue
            let bgColor = 'transparent';
            if (lastEvent.type === 'WorkflowNodeStarted') {
              color = '#eab308'; // yellow
              bgColor = 'rgba(234, 179, 8, 0.1)';
            } else if (lastEvent.type === 'WorkflowNodeCompleted') {
              color = '#22c55e'; // green
              bgColor = 'rgba(34, 197, 94, 0.1)';
            } else if (lastEvent.type === 'WorkflowNodeFailed') {
              color = '#ef4444'; // red
              bgColor = 'rgba(239, 68, 68, 0.1)';
            }
            return {
              ...node,
              style: { ...node.style, border: `2px solid ${color}`, backgroundColor: bgColor }
            };
          }
          return node;
        })
      );
    }
  }, [lastEvent, setNodes]);

  const onConnect = useCallback((params: Edge | Connection) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">System Workflow Visualization</h1>
        <p className="text-muted-foreground mt-2">
          Global architecture pipeline from Resume Ingestion to Recruiter Feedback. Future LangGraph agents will plug into this DAG.
        </p>
      </div>

      <div className="flex-1 border rounded-lg overflow-hidden bg-background">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          fitView
          colorMode="dark"
        >
          <Controls />
          <MiniMap />
          <Background variant="dots" gap={12} size={1} />
        </ReactFlow>
      </div>
    </div>
  );
}
