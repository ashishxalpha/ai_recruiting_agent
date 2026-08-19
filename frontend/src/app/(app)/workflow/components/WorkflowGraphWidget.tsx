import { Network } from "lucide-react";
import { useWorkflowGraph } from "@/hooks/useWorkflow";
import { WorkflowWidgetWrapper } from "./WorkflowWidgetWrapper";
import { ReactFlow, Background, Controls } from "@xyflow/react";
import "@xyflow/react/dist/style.css";

export function WorkflowGraphWidget({ workflowId }: { workflowId: string }) {
  const { data, isLoading, isError } = useWorkflowGraph(workflowId);

  return (
    <WorkflowWidgetWrapper
      title="Execution Graph"
      description="Topology and node execution status."
      icon={<Network className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
      contentClassName="h-[600px] p-0" // Remove padding for full-bleed graph
    >
      {(graph) => {
        const nodes = graph.nodes.map(n => {
          const isActive = graph.current_node_id === n.id;
          const isDark = true; // App is hardcoded to dark mode
          
          return {
            id: n.id,
            position: n.position,
            data: n.data,
            style: {
              backgroundColor: isDark ? '#1e293b' : '#ffffff', // slate-800 or white
              color: isDark ? '#f8fafc' : '#0f172a', // slate-50 or slate-900
              borderColor: isActive ? '#3b82f6' : (isDark ? '#334155' : '#e2e8f0'), // blue-500 or slate-700/slate-200
              borderWidth: isActive ? '2px' : '1px',
              borderStyle: 'solid',
              borderRadius: '8px',
              padding: '12px',
              width: '180px',
              textAlign: 'center' as const,
              fontWeight: isActive ? 'bold' : 'normal',
              boxShadow: isActive ? (isDark ? '0 0 15px rgba(59, 130, 246, 0.5)' : '0 4px 6px -1px rgb(0 0 0 / 0.1)') : 'none',
              transition: 'all 0.3s ease'
            }
          };
        });

        const edges = graph.edges.map(e => ({
          id: e.id,
          source: e.source,
          target: e.target,
          type: e.type || "smoothstep",
          animated: graph.current_node_id === e.target,
          style: { stroke: '#64748b', strokeWidth: 2 } // slate-500
        }));

        return (
          <div className="w-full h-full relative rounded-b-xl overflow-hidden">
            <ReactFlow
              nodes={nodes}
              edges={edges}
              fitView
              colorMode="dark"
              attributionPosition="bottom-right"
            >
              <Background gap={16} size={1} />
              <Controls />
            </ReactFlow>
          </div>
        );
      }}
    </WorkflowWidgetWrapper>
  );
}
