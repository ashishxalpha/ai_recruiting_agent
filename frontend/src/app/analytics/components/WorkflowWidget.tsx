import { GitBranch } from "lucide-react";
import { useAnalyticsWorkflow } from "@/hooks/useAnalytics";
import { AnalyticsWidgetWrapper } from "./AnalyticsWidgetWrapper";

export function WorkflowWidget() {
  const { data, isLoading, isError } = useAnalyticsWorkflow();

  return (
    <AnalyticsWidgetWrapper
      title="Workflow Analytics"
      description="LangGraph execution history and latency."
      icon={<GitBranch className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(_) => <></>}
    </AnalyticsWidgetWrapper>
  );
}
