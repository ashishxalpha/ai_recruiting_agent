import { Server } from "lucide-react";
import { useAnalyticsHealth } from "@/hooks/useAnalytics";
import { AnalyticsWidgetWrapper } from "./AnalyticsWidgetWrapper";
import { Badge } from "@/components/ui/badge";

export function PlatformHealthWidget() {
  const { data, isLoading, isError } = useAnalyticsHealth();

  return (
    <AnalyticsWidgetWrapper
      title="Platform Health"
      description="Status of underlying systems."
      icon={<Server className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(health) => {
        const components = [
          { name: "Database", val: health.database },
          { name: "Workflow Engine", val: health.workflow_engine },
          { name: "Memory Engine", val: health.memory_engine },
          { name: "Agent Runtime", val: health.agent_runtime },
          { name: "Coordination Platform", val: health.coordination_platform },
          { name: "Tool Platform", val: health.tool_platform },
          { name: "SSE", val: health.sse },
          { name: "OpenTelemetry", val: health.opentelemetry },
        ];

        return (
          <div className="space-y-4 overflow-y-auto h-full pr-2">
            {components.map((comp) => (
              <div key={comp.name} className="flex justify-between items-center border-b pb-2 last:border-0">
                <span className="text-sm font-medium">{comp.name}</span>
                <div className="flex items-center space-x-2">
                  {comp.val.latency_ms && <span className="text-xs text-muted-foreground">{comp.val.latency_ms.toFixed(1)}ms</span>}
                  <Badge variant={comp.val.status === 'healthy' ? 'default' : (comp.val.status === 'unknown' ? 'secondary' : 'destructive')}>
                    {comp.val.status}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        );
      }}
    </AnalyticsWidgetWrapper>
  );
}
