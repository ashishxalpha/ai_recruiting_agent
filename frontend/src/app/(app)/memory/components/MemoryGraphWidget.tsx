import { Network } from "lucide-react";
import { useMemoryGraph } from "@/hooks/useMemory";
import { MemoryWidgetWrapper } from "./MemoryWidgetWrapper";
import { ReactFlow, Background, Controls } from "@xyflow/react";
import "@xyflow/react/dist/style.css";

export function MemoryGraphWidget() {
  const { data, isLoading, isError } = useMemoryGraph();

  return (
    <MemoryWidgetWrapper
      title="Knowledge Graph"
      description="Topology of semantic relationships between memories."
      icon={<Network className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
      contentClassName="h-[600px] p-0"
    >
      {(graph) => {
        const nodes = graph.nodes.map(n => ({
          id: n.id,
          position: n.position,
          data: n.data,
          style: {
            border: "1px solid #e2e8f0",
            borderRadius: "8px",
            padding: "10px",
            backgroundColor: "white",
          }
        }));

        const edges = graph.edges.map(e => ({
          id: e.id,
          source: e.source,
          target: e.target,
          label: e.label,
          type: e.type || "smoothstep",
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
    </MemoryWidgetWrapper>
  );
}
