import { Clock } from "lucide-react";
import { useWorkflowTimeline } from "@/hooks/useWorkflow";
import { WorkflowWidgetWrapper } from "./WorkflowWidgetWrapper";

export function WorkflowTimelineWidget({ workflowId }: { workflowId: string }) {
  const { data, isLoading, isError } = useWorkflowTimeline(workflowId);

  return (
    <WorkflowWidgetWrapper
      title="Timeline"
      description="Lifecycle transitions."
      icon={<Clock className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(timeline) => (
        <div className="space-y-4 overflow-y-auto h-full pr-2">
           {timeline.entries.map((entry, i) => (
             <div key={entry.event_id} className="flex space-x-4">
               <div className="flex flex-col items-center">
                 <div className="w-3 h-3 bg-blue-500 rounded-full mt-1.5" />
                 {i !== timeline.entries.length - 1 && <div className="w-px h-full bg-border my-1" />}
               </div>
               <div className="pb-4">
                 <p className="text-sm font-medium">{entry.state}</p>
                 <p className="text-xs text-muted-foreground">{new Date(entry.timestamp).toLocaleString()}</p>
                 {entry.node_id && <p className="text-xs text-muted-foreground">Node: {entry.node_id}</p>}
               </div>
             </div>
           ))}
        </div>
      )}
    </WorkflowWidgetWrapper>
  );
}
