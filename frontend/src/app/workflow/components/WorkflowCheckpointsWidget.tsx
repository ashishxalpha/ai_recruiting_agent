import { History } from "lucide-react";
import { useWorkflowCheckpoints } from "@/hooks/useWorkflow";
import { WorkflowWidgetWrapper } from "./WorkflowWidgetWrapper";

export function WorkflowCheckpointsWidget({ workflowId }: { workflowId: string }) {
  const { data, isLoading, isError } = useWorkflowCheckpoints(workflowId);

  return (
    <WorkflowWidgetWrapper
      title="Checkpoints"
      description="LangGraph persistence snapshots."
      icon={<History className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(_) => <></>}
    </WorkflowWidgetWrapper>
  );
}
