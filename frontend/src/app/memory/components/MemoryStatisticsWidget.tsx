import { BarChart2 } from "lucide-react";
import { useMemoryStatistics } from "@/hooks/useMemory";
import { MemoryWidgetWrapper } from "./MemoryWidgetWrapper";

export function MemoryStatisticsWidget() {
  const { data, isLoading, isError } = useMemoryStatistics();

  return (
    <MemoryWidgetWrapper
      title="Statistics"
      description="Aggregated metrics for the memory engine."
      icon={<BarChart2 className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(_) => <></>}
    </MemoryWidgetWrapper>
  );
}
