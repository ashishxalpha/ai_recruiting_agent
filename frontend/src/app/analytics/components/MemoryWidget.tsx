import { Brain } from "lucide-react";
import { useAnalyticsMemory } from "@/hooks/useAnalytics";
import { AnalyticsWidgetWrapper } from "./AnalyticsWidgetWrapper";

export function MemoryWidget() {
  const { data, isLoading, isError } = useAnalyticsMemory();

  return (
    <AnalyticsWidgetWrapper
      title="Memory Analytics"
      description="Storage and retrieval performance."
      icon={<Brain className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(_) => <></>}
    </AnalyticsWidgetWrapper>
  );
}
