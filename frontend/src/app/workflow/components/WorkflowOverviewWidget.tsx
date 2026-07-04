import { Info } from "lucide-react";
import { useWorkflowSummary } from "@/hooks/useWorkflow";
import { WorkflowWidgetWrapper } from "./WorkflowWidgetWrapper";

export function WorkflowOverviewWidget({ workflowId }: { workflowId: string }) {
  const { data, isLoading, isError } = useWorkflowSummary(workflowId);

  return (
    <WorkflowWidgetWrapper
      title="Workflow Overview"
      description="Summary and metadata for the current execution."
      icon={<Info className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(summary) => (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm font-medium text-muted-foreground">Workflow ID</p>
              <p className="font-mono text-sm">{summary.id}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">Status</p>
              <p className="font-semibold">{summary.status}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">Version</p>
              <p>{summary.workflow_version}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-muted-foreground">Current Node</p>
              <p>{summary.current_node || "None"}</p>
            </div>
          </div>
        </div>
      )}
    </WorkflowWidgetWrapper>
  );
}
