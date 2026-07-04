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
        // Transform the DTO into React Flow formats
        const nodes = graph.nodes.map(n => ({
          id: n.id,
          position: n.position,
          data: n.data,
          style: {
            border: graph.current_node_id === n.id ? "2px solid #3b82f6" : "1px solid #e2e8f0",
            borderRadius: "8px",
            padding: "10px",
            backgroundColor: "white",
            fontWeight: graph.current_node_id === n.id ? "bold" : "normal"
          }
        }));

        const edges = graph.edges.map(e => ({
          id: e.id,
          source: e.source,
          target: e.target,
          type: e.type || "smoothstep",
          animated: graph.current_node_id === e.target
        }));

        return (
          <div className="w-full h-full">
            <ReactFlow
              nodes={nodes}
              edges={edges}
              fitView
              attributionPosition="bottom-right"
            >
              <Background />
              <Controls />
            </ReactFlow>
          </div>
        );
      }}
    </WorkflowWidgetWrapper>
  );
}
