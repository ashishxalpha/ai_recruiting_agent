import { Clock } from "lucide-react";
import { useMemoryTimeline } from "@/hooks/useMemory";
import { MemoryWidgetWrapper } from "./MemoryWidgetWrapper";

export function MemoryTimelineWidget({ memoryId }: { memoryId: string }) {
  const { data, isLoading, isError } = useMemoryTimeline(memoryId);

  return (
    <MemoryWidgetWrapper
      title="Memory Lifecycle"
      description="Timeline of events for this specific memory."
      icon={<Clock className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(_) => <></>}
    </MemoryWidgetWrapper>
  );
}
