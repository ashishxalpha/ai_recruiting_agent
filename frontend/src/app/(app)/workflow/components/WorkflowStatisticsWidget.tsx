import { BarChart2 } from "lucide-react";
import { useWorkflowStatistics } from "@/hooks/useWorkflow";
import { WorkflowWidgetWrapper } from "./WorkflowWidgetWrapper";

export function WorkflowStatisticsWidget({ workflowId }: { workflowId: string }) {
  const { data, isLoading, isError } = useWorkflowStatistics(workflowId);

  return (
    <WorkflowWidgetWrapper
      title="Statistics"
      description="Aggregated workflow metrics."
      icon={<BarChart2 className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(_) => <></>}
    </WorkflowWidgetWrapper>
  );
}
