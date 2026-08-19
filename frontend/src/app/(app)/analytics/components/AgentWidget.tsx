import { Bot } from "lucide-react";
import { useAnalyticsAgent } from "@/hooks/useAnalytics";
import { AnalyticsWidgetWrapper } from "./AnalyticsWidgetWrapper";

export function AgentWidget() {
  const { data, isLoading, isError } = useAnalyticsAgent();

  return (
    <AnalyticsWidgetWrapper
      title="Agent Analytics"
      description="Agent runtime sessions and actions."
      icon={<Bot className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(_) => <></>}
    </AnalyticsWidgetWrapper>
  );
}
