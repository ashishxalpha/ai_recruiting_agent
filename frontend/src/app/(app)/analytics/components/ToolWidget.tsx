import { Wrench } from "lucide-react";
import { useAnalyticsTools } from "@/hooks/useAnalytics";
import { AnalyticsWidgetWrapper } from "./AnalyticsWidgetWrapper";

export function ToolWidget() {
  const { data, isLoading, isError } = useAnalyticsTools();

  return (
    <AnalyticsWidgetWrapper
      title="Tool Analytics"
      description="External provider executions and latency."
      icon={<Wrench className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(_) => <></>}
    </AnalyticsWidgetWrapper>
  );
}
