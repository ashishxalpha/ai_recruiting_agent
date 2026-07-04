import { ServerCrash } from "lucide-react";
import { useWorkflowNodes } from "@/hooks/useWorkflow";
import { WorkflowWidgetWrapper } from "./WorkflowWidgetWrapper";

export function WorkflowNodesWidget({ workflowId }: { workflowId: string }) {
  const { data, isLoading, isError } = useWorkflowNodes(workflowId);

  return (
    <WorkflowWidgetWrapper
      title="Node Executions"
      description="Detailed history of node invocations."
      icon={<ServerCrash className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(_) => <></>}
    </WorkflowWidgetWrapper>
  );
}
