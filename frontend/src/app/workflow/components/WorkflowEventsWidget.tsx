import { ListTree } from "lucide-react";
import { useWorkflowEvents } from "@/hooks/useWorkflow";
import { WorkflowWidgetWrapper } from "./WorkflowWidgetWrapper";

export function WorkflowEventsWidget({ workflowId }: { workflowId: string }) {
  const { data, isLoading, isError } = useWorkflowEvents(workflowId);

  return (
    <WorkflowWidgetWrapper
      title="Event Stream"
      description="EventBus history for this execution."
      icon={<ListTree className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(_) => <></>}
    </WorkflowWidgetWrapper>
  );
}
